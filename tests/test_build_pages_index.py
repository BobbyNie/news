import importlib.util
import pathlib
import shutil
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_pages_index.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_pages_index", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BuildPagesIndexTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(self.tmpdir))

    def write_report(self, relative_path, title):
        path = self.tmpdir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"<!doctype html><html><head><title>{title}</title></head><body></body></html>",
            encoding="utf-8",
        )

    def test_discovers_reports_sorted_newest_first(self):
        module = load_module()
        self.write_report("2026-05/AI/20260526.html", "2026-05-26 AI 日报")
        self.write_report("2026-05/STOCK/20260526.html", "2026-05-26 股市日报")
        self.write_report("2026-04/AI/20260430.html", "2026-04-30 AI 日报")
        (self.tmpdir / "tmp" / "AI" / "20260526").mkdir(parents=True)
        (self.tmpdir / "tmp" / "AI" / "20260526" / "debug.html").write_text("ignore", encoding="utf-8")

        reports = module.discover_reports(self.tmpdir)

        self.assertEqual(
            [report.relative_path for report in reports],
            [
                "2026-05/AI/20260526.html",
                "2026-05/STOCK/20260526.html",
                "2026-04/AI/20260430.html",
            ],
        )

    def test_build_site_writes_index_and_copies_reports_only(self):
        module = load_module()
        self.write_report("2026-05/AI/20260526.html", "2026-05-26 AI 日报")
        self.write_report("2026-05/STOCK/20260526.html", "2026-05-26 股市日报")
        self.write_report("2026-04/STOCK/20260430.html", "2026-04-30 股市日报")
        (self.tmpdir / "tmp" / "AI" / "20260526").mkdir(parents=True)
        (self.tmpdir / "tmp" / "AI" / "20260526" / "01-raw-findings.md").write_text("raw", encoding="utf-8")

        site_dir = self.tmpdir / "public"
        module.build_site(self.tmpdir, site_dir)

        index = (site_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("2026-05-26 AI 日报", index)
        self.assertIn("2026-05-26 股市日报", index)
        self.assertLess(index.index("2026-05-26"), index.index("2026-04-30"))
        self.assertTrue((site_dir / "2026-05" / "AI" / "20260526.html").exists())
        self.assertTrue((site_dir / "2026-05" / "STOCK" / "20260526.html").exists())
        self.assertFalse((site_dir / "tmp").exists())


if __name__ == "__main__":
    unittest.main()
