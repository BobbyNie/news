from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DailyPromptUIRequirementsTest(unittest.TestCase):
    def test_ai_prompt_requires_mobile_modern_report_ui(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-ai-daily.md").read_text(encoding="utf-8")

        required = [
            "移动端 UI 设计要求",
            "AI DAILY BRIEF",
            "hero-ai",
            "top-list",
            "公司卡片",
            "scrollWidth",
            "validate_report_ui.py",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_stock_prompt_requires_mobile_market_report_ui(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-stock-daily.md").read_text(encoding="utf-8")

        required = [
            "移动端 UI 设计要求",
            "MARKET DAILY BRIEF",
            "hero-stock",
            "market-card",
            "change-up",
            "tabular-nums",
            "validate_report_ui.py",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_combined_automation_prompt_requires_ui_gate(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-automation-combined.md").read_text(encoding="utf-8")

        required = [
            "cursor-ai-daily.md",
            "cursor-stock-daily.md",
            "validate_report_ui.py",
            "max-width: 920px",
            "hero-ai",
            "hero-stock",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)


if __name__ == "__main__":
    unittest.main()
