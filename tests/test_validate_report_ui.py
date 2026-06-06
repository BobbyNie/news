from pathlib import Path
import unittest

from scripts.validate_report_ui import validate_report_html


ROOT = Path(__file__).resolve().parents[1]


class ValidateReportUITest(unittest.TestCase):
    def test_ai_report_passes_mobile_requirements(self) -> None:
        html = (ROOT / "2026-06/AI/20260605.html").read_text(encoding="utf-8")
        errors = validate_report_html(html, "AI")
        self.assertEqual(errors, [])

    def test_stock_report_passes_mobile_requirements(self) -> None:
        html = (ROOT / "2026-06/STOCK/20260603.html").read_text(encoding="utf-8")
        errors = validate_report_html(html, "STOCK")
        self.assertEqual(errors, [])

    def test_rejects_legacy_bare_template_markers(self) -> None:
        legacy = """
        <style>body { max-width: 920px; }</style>
        <body><h1>日报</h1><section id="top"><ol><li>item</li></ol></section></body>
        """
        errors = validate_report_html(legacy, "AI")
        self.assertTrue(any("920px" in error for error in errors))
        self.assertTrue(any("hero-ai" in error for error in errors))
        self.assertTrue(any("news-card" in error for error in errors))

    def test_stock_requires_change_up_and_market_card(self) -> None:
        html = """
        <header class="hero hero-stock"><p class="eyebrow">MARKET DAILY BRIEF</p></header>
        <ol class="top-list"><li class="market-card">x</li></ol>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 780px; } html { -webkit-text-size-adjust: 100%; }</style>
        """
        errors = validate_report_html(html, "STOCK")
        self.assertTrue(any("change-up" in error for error in errors))

    def test_ai_report_does_not_require_finance_sections(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        </body>
        """
        errors = validate_report_html(html, "AI")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
