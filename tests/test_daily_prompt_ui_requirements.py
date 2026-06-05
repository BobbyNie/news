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

    def test_ai_prompt_requires_finance_ai_special_topics(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-ai-daily.md").read_text(encoding="utf-8")

        required = [
            'section id="finance-ai"',
            'section id="mainland-finance-ai"',
            "金融行业 AI 专题",
            "中国内地金融行业 AI 专题",
            "核心结论",
            "可验证事件",
            "行业影响",
            "待跟踪/缺口",
            "本窗口未见可验证重大更新",
            "官方/监管/IR/交易所/主流媒体优先",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_ai_sources_include_finance_ai_seed_sources(self) -> None:
        sources = (ROOT / "sources" / "ai-sources.yaml").read_text(encoding="utf-8")

        required = [
            "financial_ai_sources",
            "BIS Innovation Hub",
            "FSB AI in finance",
            "IOSCO AI/capital markets",
            "中国人民银行金融科技规划",
            "国家金融监督管理总局数字金融/科技监管",
            "中国证监会数字金融与资本市场政策",
            "上交所/深交所官方动态",
            "financial_industry_ai",
            "mainland_financial_ai",
            "regtech_suptech",
            "ai_risk_management",
            "ai_banking_adoption",
            "ai_capital_markets",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, sources)

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

    def test_combined_automation_prompt_requires_ai_finance_topics(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-automation-combined.md").read_text(encoding="utf-8")

        required = [
            "finance-ai",
            "mainland-finance-ai",
            "金融行业 AI 专题",
            "中国内地金融行业 AI 专题",
            "官方/监管/IR/交易所/主流媒体优先",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)


if __name__ == "__main__":
    unittest.main()
