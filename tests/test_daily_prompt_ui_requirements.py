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

    def test_ai_prompt_enforces_ai_industry_content_boundary(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-ai-daily.md").read_text(encoding="utf-8")

        required = [
            "AI 行业内容边界",
            "新模型",
            "新功能",
            "Agent",
            "开发者工具",
            "开源/研究",
            "安全/治理",
            "不得把宏观、利率、股价、指数、IPO 定价或入指事件作为 AI 日报主线",
            "只有直接改变 AI 产品路线、模型能力、算力供给或企业采用时，才可作为低优先级背景",
            "窗口内缺少高可信 AI 新闻时，宁可减少条目并写明已检查来源",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

        forbidden = [
            "AI 日报必须每日固定输出两个金融行业专题",
            'section id="finance-ai"',
            'section id="mainland-finance-ai"',
        ]

        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, prompt)

    def test_ai_sources_prioritize_industry_topics_over_market_topics(self) -> None:
        sources = (ROOT / "sources" / "ai-sources.yaml").read_text(encoding="utf-8")

        required = [
            "industry_ai_adoption_sources",
            "developer_tools",
            "agent_platforms",
            "research_breakthrough",
            "enterprise_adoption",
            "industry_ai_adoption",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, sources)

        forbidden = [
            "financial_ai_sources",
            "financial_industry_ai",
            "mainland_financial_ai",
            "ai_capital_markets",
        ]

        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, sources)

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

    def test_combined_automation_prompt_requires_ai_content_boundary(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-automation-combined.md").read_text(encoding="utf-8")

        required = [
            "AI 行业内容边界",
            "新模型",
            "新功能",
            "Agent",
            "不得把宏观、利率、股价、指数、IPO 定价或入指事件作为 AI 日报主线",
            "只有直接改变 AI 产品路线、模型能力、算力供给或企业采用时，才可作为低优先级背景",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

        for text in ["finance-ai", "mainland-finance-ai"]:
            with self.subTest(text=text):
                self.assertNotIn(text, prompt)


if __name__ == "__main__":
    unittest.main()
