#!/usr/bin/env python3
"""Static checks for the English marketplace candidate.

These tests do not call a language model and do not create a PPTX.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load_packager():
    path = REPO / "scripts" / "package_agensi_candidate.py"
    spec = importlib.util.spec_from_file_location("package_agensi_candidate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packager = load_packager()

    def test_english_eval_fixtures_cover_triggers(self):
        evals = json.loads((REPO / "skills/proslide/evals/evals.json").read_text(encoding="utf-8"))
        prompts = "\n".join(item["prompt"] for item in evals["evals"])
        expected = "\n".join(item["expected_output"] for item in evals["evals"])
        for phrase in ("slide deck", "speaker notes", "PowerPoint", "PPTX", "HTML preview"):
            self.assertIn(phrase, prompts)
        self.assertIn("must not export a PPTX", expected)
        self.assertIn("not a recorded model run", expected)
        ids = [item["id"] for item in evals["evals"]]
        self.assertEqual(ids, list(range(1, 10)))

    def test_chinese_workflow_text_remains(self):
        skill = (REPO / "skills/proslide/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("强制中断点", "未经确认禁止截图或导出 PPTX", "请确认：这版 HTML 预览是否需要调整？"):
            self.assertIn(phrase, skill)
        rules = (REPO / "skills/proslide/references/layout-rules.md").read_text(encoding="utf-8")
        for color in ("#001E50", "#00B0F0", "#C00000"):
            self.assertIn(color, rules)

    def test_preview_render_matches_html_when_present(self):
        metadata_path = REPO / "marketplace" / "preview-render.json"
        if not metadata_path.is_file():
            self.skipTest("preview has not been rendered in this checkout")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        preview = (REPO / "examples/generic-english-preview/preview.html").read_bytes()
        digest = hashlib.sha256(preview).hexdigest()
        self.assertEqual(metadata["preview_sha256"], digest)
        self.assertFalse(metadata["pptx_written"])
        self.assertEqual(len(metadata["slides"]), 2)
        for slide in metadata["slides"]:
            self.assertGreaterEqual(slide["width"], 2560)
            self.assertGreaterEqual(slide["height"], 1440)

    def test_package_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.packager.build_candidate(
                REPO,
                root / "candidate.zip",
                root / "validation-report.md",
                root / "manifest.json",
            )
            self.assertLessEqual(result["zip_bytes"], 50 * 1024 * 1024)
            self.assertGreaterEqual(len(result["skills"]), 2)
            with zipfile.ZipFile(root / "candidate.zip") as archive:
                names = set(archive.namelist())
            self.assertIn("LICENSE", names)
            self.assertIn("skills/proslide/SKILL.md", names)
            self.assertIn("skills/proslide-export/scripts/export_html_to_pptx.py", names)
            self.assertNotIn("SKILL.md", names)
            self.assertNotIn("docs/INTEGRATION.md", names)
            self.assertNotIn("examples/base-slide.html", names)
            self.assertNotIn("skills/proslide/evals/evals.json", names)
            self.assertFalse(any(name.endswith(".pptx") for name in names))
            self.assertFalse(any(Path(name).name.startswith("logo.") for name in names))
            report = (root / "validation-report.md").read_text(encoding="utf-8")
            self.assertIn("not an Agensi certification", report)
            self.assertIn("中文摘要", report)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["root_skill_md"])
            self.assertEqual(len(manifest["skills"]), 6)


if __name__ == "__main__":
    unittest.main()
