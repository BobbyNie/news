from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublishToMainTest(unittest.TestCase):
    def test_publish_script_exists_and_merges_to_main(self) -> None:
        script = ROOT / "scripts" / "publish_to_main.sh"
        self.assertTrue(script.exists(), "scripts/publish_to_main.sh must exist")
        text = script.read_text(encoding="utf-8")
        for phrase in (
            "push origin main",
            "validate_report_ui.py",
            "build_pages_index.py",
            "git merge",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_publish_script_supports_weekly_reports(self) -> None:
        script = ROOT / "scripts" / "publish_to_main.sh"
        text = script.read_text(encoding="utf-8")
        for phrase in (
            "--weekly",
            "REPORT_WEEK_FILE",
            "REPORT_WEEK_MONTH",
            "tmp/WEEKLY",
            "weekly AI stock news report",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_combined_prompt_requires_publish_to_main(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-automation-combined.md").read_text(encoding="utf-8")
        self.assertIn("publish_to_main.sh", prompt)
        self.assertIn("auto-merge-daily.yml", prompt)

    def test_auto_merge_workflow_exists(self) -> None:
        workflow = ROOT / ".github" / "workflows" / "auto-merge-daily.yml"
        self.assertTrue(workflow.exists())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("cursor/**", text)
        self.assertIn("push origin main", text)

    def test_report_validation_workflow_runs_for_reader_assets(self) -> None:
        for relative_path in (
            ".github/workflows/validate-reports.yml",
            ".github/workflows/pages.yml",
        ):
            with self.subTest(relative_path=relative_path):
                workflow = ROOT / relative_path
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("assets/**", text)


if __name__ == "__main__":
    unittest.main()
