from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def latest_report(kind: str) -> Path:
    reports = sorted(ROOT.glob(f"20??-??/{kind}/*.html"))
    if not reports:
        raise AssertionError(f"No {kind} reports found")
    return reports[-1]


class LatestReportUIOutputTest(unittest.TestCase):
    def test_latest_ai_report_uses_modern_mobile_ui(self) -> None:
        html = latest_report("AI").read_text(encoding="utf-8")

        required = [
            "AI DAILY BRIEF",
            "hero-ai",
            "top-list",
            "news-card",
            "table-wrap",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, html)

    def test_latest_stock_report_uses_market_mobile_ui(self) -> None:
        html = latest_report("STOCK").read_text(encoding="utf-8")

        required = [
            "MARKET DAILY BRIEF",
            "hero-stock",
            "top-list",
            "market-card",
            "change-up",
            "table-wrap",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, html)


if __name__ == "__main__":
    unittest.main()
