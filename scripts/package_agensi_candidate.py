#!/usr/bin/env python3
"""Build the ProSlide Agensi upload candidate and write a validation report.

This command only writes local files. It does not upload, publish, or price a listing.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ZIP_EPOCH = (2026, 1, 1, 0, 0, 0)
MAX_ZIP_BYTES = 50 * 1024 * 1024
MAX_FILES = 1000
MAX_SKILLS = 50
MAX_OTHER_TEXT_FILES = 200
MAX_TEXT_CHARS = 6_000_000
MAX_SCRIPT_BYTES = 20 * 1024
MAX_NAME_CHARS = 60
MAX_SUMMARY_CHARS = 300
MIN_DEMO_CHARS = 700
MAX_DESCRIPTION_CHARS = 1024

PAYLOAD = [
    "LICENSE",
    "README.md",
    "requirements.txt",
    "docs/english-onboarding.md",
    "examples/generic-english-preview/PROMPT.md",
    "examples/generic-english-preview/preview.html",
    "examples/generic-english-preview/example-mark.svg",
    "src/export.py",
    "skills/proslide/SKILL.md",
    "skills/proslide/references/failure-recovery.md",
    "skills/proslide/references/layout-pattern-library.md",
    "skills/proslide/references/layout-rules.md",
    "skills/proslide/references/preview-qa.md",
    "skills/proslide-chart/SKILL.md",
    "skills/proslide-export/SKILL.md",
    "skills/proslide-export/scripts/export_html_to_pptx.py",
    "skills/proslide-extend/SKILL.md",
    "skills/proslide-review/SKILL.md",
    "skills/proslide-speaker-notes/SKILL.md",
]

EXCLUDED = [
    (
        "docs/INTEGRATION.md",
        "Public integration recipes are not referenced by the skills and are omitted from the buyer package.",
    ),
    (
        "examples/base-slide.html",
        "Existing starter references logo.png and the default blue styling. The generic English fixture is the sample in this package.",
    ),
    (
        "skills/proslide/evals/evals.json",
        "Repo-only trigger fixtures. Omitted so they are not injected with the skill folder. They are not a workflow resource.",
    ),
    (
        "marketplace/agensi-listing.en.md",
        "Seller-facing listing copy for the owner to paste. Not an instruction for the buyer agent.",
    ),
    (
        "scripts/package_agensi_candidate.py",
        "Maintainer packaging command. Not needed at runtime.",
    ),
    (
        "scripts/render_generic_preview.py",
        "Maintainer screenshot command. The preview PNG is a review artifact, not a package input.",
    ),
    (
        "tests/test_release_candidate.py",
        "Maintainer tests.",
    ),
]

BANNED_SUFFIXES = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".app", ".dmg", ".msi",
    ".deb", ".rpm", ".wasm", ".class", ".jar", ".war", ".pptx", ".png",
    ".jpg", ".jpeg", ".pyc", ".pyo",
}
BANNED_PARTS = {
    ".git", "__pycache__", "node_modules", "site-packages", ".venv", "venv",
    "__MACOSX",
}
SECRET_NAMES = {".env", "id_rsa", "credentials.json", "secrets.json"}
LOGO_NAMES = {"logo.png", "logo.jpg", "logo.jpeg", "logo.svg", "logo.webp"}
IMPORT_ALLOW = {"argparse", "os", "sys", "pathlib", "playwright", "pptx"}
PATH_TOKEN = re.compile(r"`([^`\n]+)`")
PATH_LIKE = re.compile(r"^(?:\.\./|\./)?[A-Za-z0-9_./-]+\.(?:md|py|html|svg|txt|json)$")
REQUIRED_PHRASES = [
    "screenshot",
    "not natively editable",
    "HTML",
    "playwright",
    "python-pptx",
    "first `.slide`",
    "50 MB",
    "skill pack",
    "example data",
    "not an Agensi certification",
    "Chromium",
    "query_selector",
]
DEMO_MARKERS = ("<!-- demonstration-input: start -->", "<!-- demonstration-input: end -->")
CHINESE_SUMMARY = """\
## 中文摘要

这是英文市场上架准备，不是上传、发布或合并。中文技能正文、默认配色和 MIT 版权说明保持原样。新增内容是英文上架文案、英文使用说明、虚构的 Northline 社区图书馆示例预览，以及可重复的打包脚本。候选 ZIP 按 2026-11-24 查阅的 Agensi 文档做成技能包：多个 SKILL.md，根目录不放 SKILL.md，体积上限 50 MB。PPTX 仍是把 `.slide` 截图铺进空白 16:9 页，文字和图表不能在 PowerPoint 里单独编辑；本候选没有导出成品 PPTX。`src/export.py` 只用 `query_selector` 导出第一个 `.slide`。没有在 Agensi 里做智能体实测，也不声称与本仓库之外的已安装版本一致。
"""


class ValidationFailure(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = errors


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_frontmatter(text: str, path: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValidationFailure([f"{path}: SKILL.md does not start with frontmatter"])
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValidationFailure([f"{path}: unterminated frontmatter"])
    return text[4:end], text[end + 5 :]


def parse_frontmatter(raw: str, path: str) -> dict[str, str]:
    data: dict[str, str] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if ":" not in line:
            raise ValidationFailure([f"{path}: cannot parse frontmatter line {line!r}"])
        key, rest = line.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if rest in {"|", ">", "|-", ">-"}:
            index += 1
            block: list[str] = []
            while index < len(lines) and (lines[index].startswith("  ") or lines[index] == ""):
                block.append(lines[index][2:] if lines[index].startswith("  ") else "")
                index += 1
            data[key] = "\n".join(block).strip()
        else:
            data[key] = rest.strip("\"'")
            index += 1
    return data


def markdown_section(text: str, heading: str) -> str:
    match = re.search(rf"^#{{2,3}} {re.escape(heading)}\s*$", text, re.M)
    if not match:
        raise ValidationFailure([f"listing is missing section {heading!r}"])
    rest = text[match.end():]
    next_heading = re.search(r"\n#{2,3} ", rest)
    body = rest[: next_heading.start()] if next_heading else rest
    return body.strip()


def demonstration_input(repo: Path) -> str:
    prompt = (repo / "examples/generic-english-preview/PROMPT.md").read_text(encoding="utf-8")
    try:
        start = prompt.index(DEMO_MARKERS[0]) + len(DEMO_MARKERS[0])
        end = prompt.index(DEMO_MARKERS[1], start)
    except ValueError as exc:
        raise ValidationFailure(["PROMPT.md is missing demonstration-input markers"]) from exc
    return prompt[start:end].strip()


def referenced_paths(text: str) -> list[str]:
    found = []
    for token in PATH_TOKEN.findall(text):
        token = token.strip()
        if PATH_LIKE.match(token):
            found.append(token)
    return found


def normalize_repo_path(path: Path) -> str | None:
    parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def resolve_reference(source: str, token: str, payload: dict[str, bytes]) -> list[str]:
    source_path = Path(source)
    raw_candidates = [source_path.parent / token, Path(token)]
    parts = source_path.parts
    if len(parts) >= 2 and parts[0] == "skills":
        raw_candidates.append(Path("skills") / parts[1] / token)
    skill_dirs = {str(Path(name).parent) for name in payload if name.endswith("SKILL.md")}
    for skill_dir in sorted(skill_dirs):
        raw_candidates.append(Path(skill_dir) / token)
    hits = []
    for candidate in raw_candidates:
        normalized = normalize_repo_path(candidate)
        if normalized in payload and normalized not in hits:
            hits.append(normalized)
    return hits


def load_payload(repo: Path) -> dict[str, bytes]:
    payload: dict[str, bytes] = {}
    missing = []
    for relative in PAYLOAD:
        path = repo / relative
        if not path.is_file():
            missing.append(relative)
            continue
        payload[relative] = path.read_bytes()
    if missing:
        raise ValidationFailure([f"missing payload file: {item}" for item in missing])
    return payload


def validate_payload(repo: Path, payload: dict[str, bytes]) -> dict:
    errors: list[str] = []
    notes: list[str] = []
    skills = []
    for relative, data in sorted(payload.items()):
        path = Path(relative)
        if any(part in BANNED_PARTS or part.startswith("._") for part in path.parts):
            errors.append(f"banned path part: {relative}")
        if path.name in SECRET_NAMES or path.name in LOGO_NAMES:
            errors.append(f"excluded sensitive or logo file: {relative}")
        if path.suffix.lower() in BANNED_SUFFIXES:
            errors.append(f"banned file type: {relative}")
        if b"BEGIN OPENSSH PRIVATE KEY" in data or b"BEGIN RSA PRIVATE KEY" in data:
            errors.append(f"private key material: {relative}")
        if path.name == "SKILL.md":
            text = data.decode("utf-8")
            raw, body = split_frontmatter(text, relative)
            meta = parse_frontmatter(raw, relative)
            name = meta.get("name", "")
            description = meta.get("description", "")
            if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
                errors.append(f"{relative}: name {name!r} is not a short lowercase skill name")
            if not description:
                errors.append(f"{relative}: description is empty")
            if len(description) > MAX_DESCRIPTION_CHARS:
                errors.append(f"{relative}: description is {len(description)} characters")
            if "English:" not in description and "English triggers:" not in description:
                errors.append(f"{relative}: description has no English trigger line")
            if name and Path(relative).parent.name != name:
                errors.append(f"{relative}: directory {Path(relative).parent.name} != name {name}")
            skills.append({"path": relative, "name": name, "description_chars": len(description)})
            if "强制中断点" not in body and name == "proslide":
                errors.append("main skill lost the Chinese hard-stop section")
            for token in referenced_paths(text):
                hits = resolve_reference(relative, token, payload)
                if not hits:
                    errors.append(f"{relative}: missing referenced path {token}")
                elif str((Path(relative).parent / token).as_posix()) not in hits:
                    notes.append(
                        f"{relative} mentions `{token}`, packaged at {', '.join(hits)}"
                    )
        if path.suffix == ".py":
            if len(data) > MAX_SCRIPT_BYTES:
                errors.append(f"{relative}: script is {len(data)} bytes; guideline is {MAX_SCRIPT_BYTES}")
            text = data.decode("utf-8")
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("import "):
                    modules = stripped.removeprefix("import ").split(",")
                    for module in modules:
                        root = module.strip().split(" as ")[0].split(".")[0]
                        if root and root not in IMPORT_ALLOW:
                            errors.append(f"{relative}: import {root} is not a standalone-script import")
                if stripped.startswith("from "):
                    root = stripped.split()[1].split(".")[0]
                    if root not in IMPORT_ALLOW:
                        errors.append(f"{relative}: from {root} is not a standalone-script import")

    export_a = payload.get("src/export.py")
    export_b = payload.get("skills/proslide-export/scripts/export_html_to_pptx.py")
    if export_a != export_b:
        errors.append("src/export.py and skills/proslide-export/scripts/export_html_to_pptx.py differ")
    if export_a and b"query_selector_all" in export_a:
        notes.append("export script now uses query_selector_all; update the listing before upload")
    if export_a and b"query_selector(" not in export_a:
        errors.append("export script no longer shows query_selector; listing text would be stale")

    sample = payload["examples/generic-english-preview/preview.html"].decode("utf-8")
    for banned in ("#001E50", "#00B0F0", "#C00000", "logo.png", "Volkswagen", "大众"):
        if banned.lower() in sample.lower():
            errors.append(f"generic preview contains {banned}")
    if sample.count('class="slide"') != 2:
        errors.append("generic preview should contain exactly two .slide elements")
    for required in ("EXAMPLE DATA", "Northline Community Library", "Hand-authored", "12", "186"):
        if required not in sample:
            errors.append(f"generic preview is missing {required}")
    if "http://" in sample or "https://" in sample:
        errors.append("generic preview links to a remote URL")

    prompt = demonstration_input(repo)
    onboarding = payload["docs/english-onboarding.md"].decode("utf-8")
    listing_path = repo / "marketplace/agensi-listing.en.md"
    if not listing_path.is_file():
        errors.append("missing marketplace/agensi-listing.en.md")
        listing = ""
    else:
        listing = listing_path.read_text(encoding="utf-8")
    for label, text in (("onboarding", onboarding), ("listing", listing)):
        for phrase in REQUIRED_PHRASES:
            if phrase not in text:
                errors.append(f"{label} is missing required phrase: {phrase}")
        if prompt not in text:
            errors.append(f"{label} does not contain the demonstration input verbatim")
    if listing:
        name = markdown_section(listing, "Name")
        summary = markdown_section(listing, "Summary")
        demo = markdown_section(listing, "See it in action")
        if "\n" in name:
            errors.append("listing name must be a single line")
        if len(name) > MAX_NAME_CHARS or not name:
            errors.append(f"listing name length is {len(name)}")
        if len(summary) > MAX_SUMMARY_CHARS or not summary:
            errors.append(f"listing summary length is {len(summary)}")
        if len(demo) < MIN_DEMO_CHARS:
            errors.append(f"See it in action is {len(demo)} characters; form guidance prefers 700+")
        if "not a recorded agent transcript" not in demo:
            errors.append("See it in action must say it is not a recorded agent transcript")

    license_text = payload["LICENSE"].decode("utf-8")
    if "MIT License" not in license_text or "Copyright (c) 2026 ProSlide Contributors" not in license_text:
        errors.append("LICENSE text is not the repository MIT copyright notice")
    readme = payload["README.md"].decode("utf-8")
    if not readme.startswith("# ProSlide\n"):
        errors.append("README H1 is not ProSlide; Agensi uses that heading as the pack name")
    requirements = payload["requirements.txt"].decode("utf-8")
    if "playwright" not in requirements or "python-pptx" not in requirements:
        errors.append("requirements.txt does not declare playwright and python-pptx")
    if "SKILL.md" not in {Path(item).name for item in payload} or any(item == "SKILL.md" for item in payload):
        errors.append("unexpected root SKILL.md; this candidate is a pack and intentionally has none")
    if len(skills) < 2 or len(skills) > MAX_SKILLS:
        errors.append(f"skill count {len(skills)} is outside 2..{MAX_SKILLS}")

    other_text = [item for item in payload if not item.endswith("SKILL.md")]
    text_chars = sum(len(data.decode("utf-8")) for data in payload.values())
    if len(other_text) > MAX_OTHER_TEXT_FILES:
        errors.append("too many non-SKILL text files for the documented buyer delivery cap")
    if text_chars > MAX_TEXT_CHARS:
        errors.append("packaged text exceeds the documented 6 million character delivery cap")

    if errors:
        raise ValidationFailure(errors)
    return {
        "skills": skills,
        "notes": notes,
        "other_text_files": len(other_text),
        "text_chars": text_chars,
        "listing_name": markdown_section(listing, "Name"),
        "listing_summary_chars": len(markdown_section(listing, "Summary")),
        "listing_demo_chars": len(markdown_section(listing, "See it in action")),
        "demonstration_input": prompt,
    }


def packaging_text(info: dict) -> str:
    skill_lines = "\n".join(f"- {item['name']}: {item['path']}" for item in info["skills"])
    return (
        "ProSlide Agensi upload candidate\n"
        "This ZIP is a local release candidate. It is not an Agensi certification,\n"
        "not a published release, and not evidence that a live agent was tested.\n\n"
        "Layout: skill pack. SKILL.md files live under skills/. There is no root SKILL.md.\n"
        "Agensi docs checked 2026-11-24 say a pack does not need a root SKILL.md.\n"
        "https://www.agensi.io/docs/packaging\n\n"
        "License: MIT. Copyright (c) 2026 ProSlide Contributors. See LICENSE.\n\n"
        "Skills:\n"
        f"{skill_lines}\n\n"
        "English map: docs/english-onboarding.md\n"
        "Example preview (hand-authored, example data, not a finished PPTX):\n"
        "examples/generic-english-preview/\n\n"
        "Export script: skills/proslide-export/scripts/export_html_to_pptx.py\n"
        "It is a byte copy of src/export.py. It screenshots the first .slide only\n"
        "and places that raster image on a blank 16:9 slide. The HTML remains the\n"
        "editable source. Text in the PPTX is not natively editable.\n"
        "Dependencies are declared in requirements.txt and are not bundled:\n"
        "playwright, python-pptx, and a Chromium browser.\n"
        "No Agensi paid tool or API key is required by these files.\n"
    )


def manifest_document(payload: dict[str, bytes], info: dict) -> dict:
    files = []
    for name in sorted(payload):
        files.append({
            "path": name,
            "bytes": len(payload[name]),
            "sha256": sha256_bytes(payload[name]),
        })
    return {
        "package": "proslide-agensi-candidate",
        "kind": "skill-pack",
        "root_skill_md": False,
        "root_skill_md_note": "Omitted on purpose. Agensi docs checked 2026-11-24 say two or more SKILL.md files form a pack and a root SKILL.md is not required.",
        "docs_checked": [
            "https://www.agensi.io/docs/packaging",
            "https://www.agensi.io/docs/submit-on-the-website",
            "https://www.agensi.io/docs/creator-faq",
            "https://www.agensi.io/docs/what-you-can-sell",
        ],
        "skills": info["skills"],
        "files": files,
        "excluded": [{"path": path, "reason": reason} for path, reason in EXCLUDED],
        "self": "PACKAGING-MANIFEST.json is added after this file list. The validation report inventories every ZIP member, including this manifest.",
    }


def build_zip(payload: dict[str, bytes], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        for name in sorted(payload):
            info = zipfile.ZipInfo(filename=name, date_time=ZIP_EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload[name])
        archive.comment = b"ProSlide Agensi release candidate. Not a published release."


def render_report(repo: Path, zip_path: Path, payload: dict[str, bytes], info: dict, zip_members: list[dict]) -> str:
    zip_bytes = zip_path.read_bytes()
    preview_path = repo / "marketplace/preview-render.json"
    if preview_path.is_file():
        preview = json.loads(preview_path.read_text(encoding="utf-8"))
        preview_block = json.dumps(preview, indent=2, ensure_ascii=False)
    else:
        preview_block = "No marketplace/preview-render.json yet. Run python3 scripts/render_generic_preview.py."
    skill_rows = "\n".join(
        f"| {item['name']} | {item['path']} | {item['description_chars']} |"
        for item in info["skills"]
    )
    member_rows = "\n".join(
        f"| `{item['path']}` | {item['bytes']} | `{item['sha256']}` |"
        for item in zip_members
    )
    excluded_rows = "\n".join(f"| `{path}` | {reason} |" for path, reason in EXCLUDED)
    note_lines = "\n".join(f"- {note}" for note in info["notes"]) or "- None."
    return f"""# ProSlide Agensi candidate validation report

Generated by `python3 scripts/package_agensi_candidate.py`.
This report checks files and the ZIP. It is not an Agensi certification, not an upload receipt, and not a model evaluation.

## Result

- ZIP: `{zip_path.name}`
- ZIP bytes: {len(zip_bytes)} (limit {MAX_ZIP_BYTES})
- ZIP sha256: `{sha256_bytes(zip_bytes)}`
- Members: {len(zip_members)} (website file limit {MAX_FILES})
- Skills: {len(info['skills'])} (pack range 2–{MAX_SKILLS})
- Root SKILL.md: no, by design
- Other text files besides SKILL.md in the payload: {info['other_text_files']} (documented buyer cap {MAX_OTHER_TEXT_FILES})
- Payload text characters: {info['text_chars']} (documented cap {MAX_TEXT_CHARS})
- Listing name: {info['listing_name']} ({len(info['listing_name'])}/{MAX_NAME_CHARS})
- Listing summary characters: {info['listing_summary_chars']}/{MAX_SUMMARY_CHARS}
- See it in action characters: {info['listing_demo_chars']} (guidance {MIN_DEMO_CHARS}+)
- Export copies identical: yes (`src/export.py` and `skills/proslide-export/scripts/export_html_to_pptx.py`)

## Environment

- Python: {sys.version.split()[0]}
- Platform: {sys.platform}
- Repository validation time: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
- Docs checked on 2026-11-24: packaging, submit-on-the-website, creator-faq, what-you-can-sell

## Tests this report represents

- Frontmatter `name` and `description` on every packaged SKILL.md
- English trigger line present in every packaged description
- Chinese hard-stop section still present in `skills/proslide/SKILL.md`
- Referenced backtick paths resolve to a packaged file
- Generic preview has two slides, example-data labels, no default brand hex colors, no `logo.png`, no remote URL
- Demonstration input is identical in `PROMPT.md`, the English onboarding, and the listing
- Listing name, summary, and demonstration length
- MIT copyright notice preserved
- Script size under 20 KB and no local-module import
- ZIP size, file count, banned types, secrets, logos, caches, and bundled dependency directories
- No PPTX member

Static English trigger fixtures live in `skills/proslide/evals/evals.json` and `tests/test_release_candidate.py`. They were not sent to a model. No LLM end-to-end run was performed. No Agensi agent session was opened.

## Skills

| Name | Path | Description characters |
|---|---|---|
{skill_rows}

## Cross-references

{note_lines}

The export path is mentioned from the main skill as `scripts/export_html_to_pptx.py` and is packaged under `skills/proslide-export/`. The prose in the main skill calls it the export skill's script.

## Export behavior checked against source

`src/export.py` launches Chromium at 1280×720 with device scale 2, waits 1000ms, screenshots the first `.slide` via `query_selector`, and inserts that PNG at full slide width on one 16:9 slide. Height is not passed. The installed python-pptx docstring says that omitting height preserves the image aspect ratio, and `slide_layouts[6]` on its default template is named Blank. That was checked without writing a PPTX. The temporary PNG is deleted by the script. `references/failure-recovery.md` asks for every slide, both dimensions, and a higher scale. Those recovery instructions are stricter than the script. The listing states the script's behavior. This command did not write a PPTX.

## ZIP members

| Path | Bytes | SHA256 |
|---|---|---|
{member_rows}

## Excluded from the ZIP

| Path | Reason |
|---|---|
{excluded_rows}

Screenshots, if rendered, stay outside the ZIP. Agensi's packaging doc says agents receive text, and the HTML source is the text form of the preview.

## Preview render metadata

```json
{preview_block}
```

## Unresolved compatibility

- Agensi name uniqueness for ProSlide was not checked. No account action was taken.
- The 32 marketplace categories were not copied. The owner chooses up to three on the form.
- A buyer session's permission to launch Chromium, read `file://` HTML, and install playwright was not tested. The script needs all three. Dependencies are not bundled.
- In-agent upload (100 files, 5 MB, text only) is a different channel. This ZIP targets the website limit of 50 MB.
- This repository may differ from a newer skill installed outside it. No parity claim is made.
- Default colors `#001E50`, `#00B0F0`, and `#C00000` remain in the Chinese layout rules. Only the new generic sample avoids them.
- Whether the buyer agent preserves the `docs/english-onboarding.md` path, or only receives the file body as a shared text, was not observed. Current docs say shared files outside skill folders are delivered with each loaded skill.

## Reproduce

```bash
python3 -m unittest tests.test_release_candidate
python3 scripts/render_generic_preview.py
python3 scripts/package_agensi_candidate.py
```

{CHINESE_SUMMARY}
"""


def build_candidate(repo: Path, zip_path: Path, report_path: Path, manifest_path: Path) -> dict:
    payload = load_payload(repo)
    info = validate_payload(repo, payload)
    manifest = manifest_document(payload, info)
    manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    packaged = dict(payload)
    packaged["PACKAGING.txt"] = packaging_text(info).encode("utf-8")
    packaged["PACKAGING-MANIFEST.json"] = manifest_bytes
    build_zip(packaged, zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        members = []
        for item in sorted(archive.infolist(), key=lambda entry: entry.filename):
            data = archive.read(item.filename)
            members.append({
                "path": item.filename,
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            })
            if item.filename.startswith("__MACOSX") or item.filename.endswith(".DS_Store"):
                raise ValidationFailure([f"archive contains {item.filename}"])
    if zip_path.stat().st_size > MAX_ZIP_BYTES:
        raise ValidationFailure([f"ZIP is {zip_path.stat().st_size} bytes"])
    if len(members) > MAX_FILES:
        raise ValidationFailure([f"ZIP has {len(members)} files"])
    report = render_report(repo, zip_path, packaged, info, members)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(manifest_bytes.decode("utf-8"), encoding="utf-8")
    return {
        "zip_path": str(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": sha256_bytes(zip_path.read_bytes()),
        "members": members,
        "skills": info["skills"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Package the ProSlide Agensi release candidate")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--zip", type=Path, default=REPO / "dist" / "proslide-agensi-candidate.zip")
    parser.add_argument("--report", type=Path, default=REPO / "marketplace" / "validation-report.md")
    parser.add_argument("--manifest", type=Path, default=REPO / "marketplace" / "manifest.json")
    args = parser.parse_args()
    if not filecmp.cmp(args.repo / "src" / "export.py", args.repo / "skills" / "proslide-export" / "scripts" / "export_html_to_pptx.py", shallow=False):
        print("export scripts differ; refresh the skill copy from src/export.py", file=sys.stderr)
        return 1
    try:
        result = build_candidate(args.repo, args.zip, args.report, args.manifest)
    except ValidationFailure as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Wrote {result['zip_path']} ({result['zip_bytes']} bytes)")
    print(f"sha256 {result['zip_sha256']}")
    print(f"Wrote {args.report}")
    print(f"Wrote {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
