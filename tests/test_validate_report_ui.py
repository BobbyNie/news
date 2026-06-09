from pathlib import Path
import subprocess
import sys
import unittest

from scripts.validate_report_ui import latest_reports, validate_report_html


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

    def test_ai_report_requires_finance_ai_applications_column(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        </body>
        """
        errors = validate_report_html(html, "AI")
        self.assertTrue(any("finance-ai-applications" in error for error in errors))

    def test_ai_report_accepts_finance_ai_applications_column(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <section id="finance-ai-applications"><h2>金融业 AI 应用专栏（银行优先）</h2></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        </body>
        """
        errors = validate_report_html(html, "AI")
        self.assertEqual(errors, [])

    def test_future_ai_report_requires_read_aloud_controls(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <section id="finance-ai-applications"><h2>金融业 AI 应用专栏（银行优先）</h2></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        </body>
        """
        errors = validate_report_html(html, "AI", report_date="20260608")
        self.assertTrue(any("reader-controls" in error for error in errors))

    def test_future_ai_report_accepts_shared_reader_module(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <div class="reader-controls" data-reader-controls>
          <button type="button" data-reader-start>朗读</button>
          <button type="button" data-reader-pause>暂停</button>
          <button type="button" data-reader-resume>继续</button>
          <button type="button" data-reader-stop>停止</button>
          <button type="button" data-reader-settings-open aria-label="设置">⚙</button>
          <p data-reader-status>可使用浏览器语音朗读本文。</p>
          <dialog data-reader-settings>
            <button type="button" data-reader-settings-close>关闭</button>
            <input type="password" data-google-tts-key>
            <select data-google-tts-voice></select>
            <button type="button" data-google-tts-save>保存 Key</button>
            <button type="button" data-google-tts-clear>清除 Key</button>
          </dialog>
        </div>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <section id="finance-ai-applications"><h2>金融业 AI 应用专栏（银行优先）</h2></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        <script src="../../assets/report-reader.js" defer></script>
        </body>
        """
        errors = validate_report_html(html, "AI", report_date="20260608")
        self.assertEqual(errors, [])

    def test_future_ai_report_requires_shared_reader_script(self) -> None:
        html = """
        <body class="report report-ai">
        <header class="hero hero-ai"><p class="eyebrow">AI DAILY BRIEF</p></header>
        <div class="reader-controls" data-reader-controls>
          <button type="button" data-reader-start>朗读</button>
          <button type="button" data-reader-settings-open aria-label="设置">⚙</button>
          <dialog data-reader-settings>
            <input type="password" data-google-tts-key>
            <select data-google-tts-voice></select>
            <button type="button" data-google-tts-save>保存 Key</button>
            <button type="button" data-google-tts-clear>清除 Key</button>
          </dialog>
        </div>
        <section id="top"><ol class="top-list"><li class="news-card">x</li></ol></section>
        <section id="finance-ai-applications"><h2>金融业 AI 应用专栏（银行优先）</h2></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 760px; } html { -webkit-text-size-adjust: 100%; }</style>
        </body>
        """
        errors = validate_report_html(html, "AI", report_date="20260608")
        self.assertTrue(any("report-reader.js" in error for error in errors))

    def test_future_weekly_report_requires_weekly_reader_script_path(self) -> None:
        html = """
        <body class="report report-weekly">
        <header class="hero hero-weekly"><p class="eyebrow">AI + MARKET WEEKLY BRIEF</p></header>
        <div class="reader-controls" data-reader-controls>
          <button type="button" data-reader-start>朗读</button>
          <button type="button" data-reader-settings-open aria-label="设置">⚙</button>
          <dialog data-reader-settings>
            <input type="password" data-google-tts-key>
            <select data-google-tts-voice></select>
            <button type="button" data-google-tts-save>保存 Key</button>
            <button type="button" data-google-tts-clear>清除 Key</button>
          </dialog>
        </div>
        <section id="top"><ol class="top-list"><li class="weekly-card">x</li></ol></section>
        <div class="table-wrap"><table></table></div>
        <style>body { max-width: 800px; } html { -webkit-text-size-adjust: 100%; }</style>
        <script src="../../assets/report-reader.js" defer></script>
        </body>
        """
        errors = validate_report_html(html, "WEEKLY", report_date="20260614")
        self.assertTrue(any("../assets/report-reader.js" in error for error in errors))

    def test_weekly_report_passes_mobile_requirements(self) -> None:
        html = (ROOT / "2026-06/2026-W23.html").read_text(encoding="utf-8")
        errors = validate_report_html(html, "WEEKLY", report_date="20260607")
        self.assertEqual(errors, [])

    def test_latest_reports_include_weekly_report(self) -> None:
        reports = latest_reports(ROOT)
        self.assertIn("WEEKLY", {report.kind for report in reports})

    def test_cli_validates_weekly_report_by_week(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_report_ui.py"),
                "--root",
                str(ROOT),
                "--kind",
                "WEEKLY",
                "--date",
                "2026-W23",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
