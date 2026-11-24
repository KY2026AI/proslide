#!/usr/bin/env python3
"""Render the generic English HTML preview to PNG screenshots.

This does not call the PPTX exporter and does not write a .pptx file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SLIDE_RE = re.compile(r'<section class="slide"[\s\S]*?</section>')
STYLE_RE = re.compile(r"<style>([\s\S]*?)</style>")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"{path} is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def chrome_binary() -> str:
    # Prefer the real binary. A wrapper that pins --remote-debugging-port and a
    # shared user-data-dir will hang a second headless screenshot.
    for candidate in ("/usr/bin/google-chrome-stable", "/opt/google/chrome/chrome"):
        if Path(candidate).is_file():
            return candidate
    for name in ("chromium", "chromium-browser", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("no Chrome or Chromium binary found")


def single_slide_html(style: str, slide: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
{style}
body {{ margin: 0; background: #fff; }}
</style>
</head>
<body>
{slide}
</body>
</html>
"""


def render(repo: Path, output_dir: Path) -> dict:
    preview = repo / "examples" / "generic-english-preview" / "preview.html"
    mark = repo / "examples" / "generic-english-preview" / "example-mark.svg"
    html = preview.read_text(encoding="utf-8")
    style_match = STYLE_RE.search(html)
    slides = SLIDE_RE.findall(html)
    if not style_match or len(slides) != 2:
        raise RuntimeError("preview.html did not contain one style block and two slides")
    output_dir.mkdir(parents=True, exist_ok=True)
    chrome = chrome_binary()
    version = subprocess.check_output([chrome, "--version"], text=True).strip()
    outputs = []
    with tempfile.TemporaryDirectory(prefix="proslide-preview-") as tmp:
        tmp_path = Path(tmp)
        shutil.copy(mark, tmp_path / "example-mark.svg")
        for index, slide in enumerate(slides, start=1):
            page = tmp_path / f"slide-{index}.html"
            page.write_text(single_slide_html(style_match.group(1), slide), encoding="utf-8")
            destination = output_dir / f"generic-english-preview-slide-{index}.png"
            if destination.exists():
                destination.unlink()
            command = [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--hide-scrollbars",
                "--no-first-run",
                f"--user-data-dir={tmp_path / 'chrome-profile'}",
                "--force-device-scale-factor=2",
                "--window-size=1280,720",
                "--default-background-color=FFFFFFFF",
                "--virtual-time-budget=4000",
                f"--screenshot={destination.resolve()}",
                page.as_uri(),
            ]
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if not destination.is_file():
                raise RuntimeError(f"Chrome did not write {destination}")
            width, height = png_size(destination)
            outputs.append({
                "file": destination.name,
                "bytes": destination.stat().st_size,
                "width": width,
                "height": height,
                "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            })
    metadata = {
        "renderer": chrome,
        "renderer_version": version,
        "device_scale_factor": 2,
        "viewport": "1280x720",
        "pptx_written": False,
        "note": "Hand-authored HTML rendered locally. Not an agent transcript and not a PPTX export.",
        "preview_sha256": hashlib.sha256(preview.read_bytes()).hexdigest(),
        "slides": outputs,
    }
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description="Screenshot the generic English preview")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--output-dir", type=Path, default=REPO / "dist" / "preview")
    parser.add_argument("--metadata", type=Path, default=REPO / "marketplace" / "preview-render.json")
    args = parser.parse_args()
    metadata = render(args.repo, args.output_dir)
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
