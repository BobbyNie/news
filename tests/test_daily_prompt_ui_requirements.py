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
            "语音朗读",
            "reader-controls",
            "data-reader-controls",
            "speechSynthesis",
            "SpeechSynthesisUtterance",
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

        forbidden = ["AI 日报必须每日固定输出两个金融行业专题"]

        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, prompt)

    def test_ai_prompt_requires_banking_first_finance_ai_applications_column(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-ai-daily.md").read_text(encoding="utf-8")

        required = [
            'section id="finance-ai-applications"',
            "金融业 AI 应用专栏（银行优先）",
            "银行、券商、保险、资管、支付、交易所、监管科技",
            "银行新服务",
            "客户服务",
            "财富管理",
            "风控/反欺诈",
            "信贷审批",
            "合规/监管科技",
            "内部开发者工具",
            "AI 基础设施建设",
            "没有可验证银行或金融机构 AI 应用更新时，保留专栏并写明已检查来源",
            "不得用宏观、利率、股价、指数、IPO 定价、入指事件、金融就业或券商观点填充",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_ai_sources_prioritize_industry_topics_over_market_topics(self) -> None:
        sources = (ROOT / "sources" / "ai-sources.yaml").read_text(encoding="utf-8")

        required = [
            "industry_ai_adoption_sources",
            "banking_and_finance_ai",
            "HSBC and AI",
            "Bank of America Erica",
            "DBS AI banking",
            "JPMorganChase AI",
            "developer_tools",
            "agent_platforms",
            "research_breakthrough",
            "enterprise_adoption",
            "industry_ai_adoption",
            "banking_ai_applications",
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
            "语音朗读",
            "reader-controls",
            "data-reader-controls",
            "speechSynthesis",
            "SpeechSynthesisUtterance",
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
            "语音朗读",
            "reader-controls",
            "data-reader-controls",
            "speechSynthesis",
            "SpeechSynthesisUtterance",
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
            "金融业 AI 应用专栏（银行优先）",
            "银行新服务",
            "不得把宏观、利率、股价、指数、IPO 定价或入指事件作为 AI 日报主线",
            "只有直接改变 AI 产品路线、模型能力、算力供给或企业采用时，才可作为低优先级背景",
            "不得用宏观、利率、股价、指数、IPO 定价、入指事件、金融就业或券商观点填充",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_weekly_prompt_requires_combined_weekly_report_workflow(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-weekly.md").read_text(encoding="utf-8")

        required = [
            "AI + 股市周报",
            "每周日",
            "automation_trigger_info.triggeredAt",
            "Asia/Macau",
            "REPORT_WEEK_FILE",
            "YYYY-Www.html",
            "cursor-ai-daily.md",
            "cursor-stock-daily.md",
            "移动端 UI 设计要求",
            "AI 行业内容边界",
            "不提供买卖建议",
            "语音朗读",
            "reader-controls",
            "data-reader-controls",
            "speechSynthesis",
            "SpeechSynthesisUtterance",
            "python3 scripts/build_pages_index.py",
            "index.html",
            "publish_to_main.sh --weekly",
            "weekly AI stock news report",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)

    def test_weekly_prompt_integrates_existing_daily_reports(self) -> None:
        prompt = (ROOT / "prompts" / "cursor-weekly.md").read_text(encoding="utf-8")

        required = [
            "先读取本周已生成的每日 AI 日报与股市日报",
            "${REPORT_WEEK_MONTH}/AI/YYYYMMDD.html",
            "${REPORT_WEEK_MONTH}/STOCK/YYYYMMDD.html",
            "tmp/AI/YYYYMMDD/02-ranked-items.md",
            "tmp/AI/YYYYMMDD/03-draft-cn.md",
            "tmp/STOCK/YYYYMMDD/02-ranked-items.md",
            "tmp/STOCK/YYYYMMDD/03-draft-cn.md",
            "tmp/WEEKLY/${REPORT_WEEK_FILE}/01-daily-report-rollup.md",
            "不得跳过既有日報只重新检索",
            "日報已经覆盖过的事实",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, prompt)


if __name__ == "__main__":
    unittest.main()
