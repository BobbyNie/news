# Cursor Automation Prompt: AI 日报

你在 `/Users/bobbynie/gitStore/news` 工作。请生成今日 AI 新闻中文 HTML 日报。

## 日期与时间（必须先执行）

Automation 定时为 **UTC 23:00**（= 澳门次日 **07:00**）。**禁止**直接使用系统注入的 `Today's date`（常为 UTC，会比澳门早一天）。

1. 读取 `automation_trigger_info.triggeredAt`（ISO-8601 UTC）。
2. 换算为 **Asia/Macau (UTC+8)**，得到报告日期 `YYYYMMDD` 与 `YYYY-MM-DD`。
3. 所有路径中的 `YYYYMMDD`、`YYYY-MM`、HTML 标题、commit message 日期，一律用**澳门日历日**。
4. HTML「生成时间」= 上述澳门本地时刻（取自 `triggeredAt`，**禁止**手工编造如 23:05）。
5. 「采集窗口」= 生成时刻往前 **48 小时** 至生成时刻（澳门时间，格式 `YYYY-MM-DD HH:MM ~ YYYY-MM-DD HH:MM`）。

可运行辅助脚本核对（将 `<TRIGGERED_AT>` 替换为实际值）：

```bash
python scripts/report_date.py <TRIGGERED_AT>
```

示例：`2026-05-27T23:02:33.581Z` → 报告日 `20260528`，生成时间 `2026-05-28 07:02（澳门时间）`，窗口 `2026-05-26 07:02 ~ 2026-05-28 07:02`。

严格按以下步骤执行：

0. **必须先运行** `eval "$(python3 scripts/report_date.py)"`，用输出的 `REPORT_DATE` / `REPORT_ISO` / `REPORT_MONTH` / `REPORT_WINDOW` 作为唯一日期依据。**禁止使用 UTC 或系统默认时区日期**（UTC 23:00 时澳门已是次日）。
1. 读取 `sources/ai-sources.yaml` 和 `sources/source-review-rules.md`。
2. 先重检清单：搜索过去 24-48 小时是否有新的重点 AI 公司、官方来源、模型/产品发布页、开发者文档、X/Facebook 官方账号、主流媒体专题、论坛或研究社区需要加入跟踪；除非直接对应 AI 产品、模型、开发者工具或企业采用，不新增金融、股票、宏观或纯资本市场来源。把结果写入 `tmp/AI/YYYYMMDD/00-source-review.md`。
3. 按清单检索官方博客、RSS、新闻稿、主流媒体、X/Facebook、论坛、研究社区，以及 `industry_ai_adoption_sources` 中与 AI 实际落地直接相关的行业来源。公开官方来源优先，X/Facebook 仅作为补充，必须验证官方账号。把原始发现写入 `tmp/AI/YYYYMMDD/01-raw-findings.md`。
4. 按下方 **「AI 行业内容边界」** 去重、分级、排序，把候选新闻写入 `tmp/AI/YYYYMMDD/02-ranked-items.md`。
5. 生成中文草稿到 `tmp/AI/YYYYMMDD/03-draft-cn.md`。
6. **生成 HTML 前**必须完整阅读本文件 **「移动端 UI 设计要求」** 与 **HTML 结构** 章节；以 `2026-06/AI/20260602.html` 为结构参考，**禁止**复用 `max-width: 920px` 旧模板。
7. 用中文生成 HTML 报告到 `YYYY-MM/AI/YYYYMMDD.html`。报告必须包含：今日最重要 5-10 条、主题详情、模型/产品/Agent/开发者工具主线、公司跟踪表、风险与不确定性、明日继续跟踪、来源覆盖与缺口。
8. **HTML 生成后**运行 `python3 scripts/validate_report_ui.py --kind AI --date YYYYMMDD`，失败则修正后重跑，**通过才可 commit**。
9. 每条重要判断必须附来源链接。不要编造无法验证的信息。
10. 完成后运行 `python3 scripts/build_pages_index.py` 更新根目录 `index.html`。
11. **必须** `git add`、`git commit`（message: `daily AI news report ${REPORT_ISO}`）。若与股市日报同一次 Automation，先完成本步再处理 STOCK；**最终**运行 `./scripts/publish_to_main.sh '<TRIGGERED_AT>'` 合并到 `main` 并 `git push origin main`（禁止只留在 `cursor/*` 分支）。
12. 确认 `main` push 成功；GitHub Actions `Publish News Pages` 会在 push 到 `main` 后自动部署 Pages。备用：仅 push 功能分支时由 `auto-merge-daily.yml` 自动合并。

## 输出要求

- **报告日期与文件名必须使用澳门时区**，且以 `automation_trigger_info.triggeredAt` 换算结果为准（见上文「日期与时间」）。
- 英文来源需翻译成中文并保留原文链接。
- 重要判断必须有可点击来源链接。
- X/Facebook 内容只作为补充信号，除非能确认官方账号。
- 无法访问的来源要在“来源覆盖与缺口”列出。
- 不写投资建议。

## AI 行业内容边界

AI 日报的主线必须是 AI 行业进展，而不是股市日报、宏观日报或 IPO 日报的延伸。

- P0/P1 优先给直接 AI 新闻：新模型、新功能、Agent 与自动化产品、开发者工具/API、开源/研究、企业或行业 AI 采用、算力/芯片/云服务的能力与供给变化、安全/治理、重大公司产品路线调整。
- 不得把宏观、利率、股价、指数、IPO 定价或入指事件作为 AI 日报主线；这些内容默认归股市日报。
- 只有直接改变 AI 产品路线、模型能力、算力供给或企业采用时，才可作为低优先级背景；写法必须落到 AI 能力、交付、供给、采用或治理，不写交易结论。
- 上市公司财报、IR、融资、并购或 IPO 只在披露了可验证的 AI 产品、模型、算力、客户采用或研发投入变化时进入 AI 日报；不得以股价涨跌、估值、募资规模、指数调仓或资金流作为入选理由。
- 金融行业 AI 只作为行业应用案例处理：必须是可验证的 AI 系统上线、模型风险治理、监管科技或金融机构真实采用；不得固定每日输出金融专题，也不得用金融就业、港股指数、券商观点补位。
- 窗口内缺少高可信 AI 新闻时，宁可减少条目并写明已检查来源，不要用宏观、行情或 IPO 噪音凑满 5-10 条。

## 移动端 UI 设计要求

报告必须是 mobile-first 的单文件 HTML/CSS，适合手机阅读，且保留现代 AI 报告感。禁止生成只有默认 `h1/table/ul` 的裸 HTML。

- 视觉方向：现代、冷静、科技报告感；首屏深色标题区，正文浅色背景，蓝色/青色作为少量强调色。不要使用大面积紫色渐变、装饰性光球或营销落地页风格。
- 页面宽度：`body` 最大宽度约 `760px`，手机左右 padding 约 `18px`，正文 `font-size: 16px` 起、`line-height: 1.65` 左右。
- 首屏：使用 `<header class="hero hero-ai">`，包含英文眉标 `AI DAILY BRIEF`、`h1`、一句报告说明、生成时间和采集窗口。时间必须来自 `REPORT_GENERATED_AT` / `REPORT_WINDOW`。
- 今日重点：`#top` 内使用 `<ol class="top-list">`，每条为 `<li class="news-card">`，用序号块、标题、影响说明、状态标签和来源链接呈现，不要让长新闻堆成一整段。
- 内容结构：分主题详情用短段落和小标题；风险、缺口用醒目的 `.warn` 区块；链接必须便于手机点击。
- 公司跟踪表：手机端优先用“公司卡片”（例如 `.company-card`）展示公司、动态、状态、来源；如果使用表格，必须包在 `<div class="table-wrap">` 中允许内部横向滚动。
- 表格与宽内容：`table` 不得撑破页面，必须通过 `.table-wrap { overflow-x: auto; }` 处理。
- 浏览器自检：生成后用 390px 手机宽度检查 `document.documentElement.scrollWidth <= window.innerWidth`；只有 `.table-wrap` 内部允许横向滚动。
- 所有 CSS 必须内联在 `<style>`，不依赖外部字体、JS 或远程资源。

建议使用以下视觉基底，可按内容轻微调整但必须保留类名：

```css
:root {
  --paper: #f6f8fb;
  --ink: #111827;
  --muted: #667085;
  --line: #d9e2ef;
  --surface: #ffffff;
  --accent: #2563eb;
  --accent-2: #0891b2;
  --warning-bg: #fff7ed;
  --warning-line: #f59e0b;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0 auto;
  max-width: 760px;
  min-height: 100vh;
  padding: 0 18px 44px;
  background:
    linear-gradient(180deg, #eaf1ff 0, rgba(234, 241, 255, 0) 360px),
    repeating-linear-gradient(90deg, rgba(17, 24, 39, 0.035) 0, rgba(17, 24, 39, 0.035) 1px, transparent 1px, transparent 44px),
    var(--paper);
  color: var(--ink);
  font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", sans-serif;
  font-size: 16px;
  line-height: 1.68;
  letter-spacing: 0;
}
.hero-ai {
  margin: 0 -18px;
  padding: 28px 18px 18px;
  background: #0f172a;
  color: #f8fafc;
  border-bottom: 4px solid var(--accent-2);
}
.eyebrow {
  margin: 0 0 12px;
  color: #93c5fd;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}
h1 { margin: 0; font-size: clamp(1.78rem, 8vw, 2.4rem); line-height: 1.12; letter-spacing: 0; }
.lead { margin: 12px 0 0; color: #dbeafe; }
.meta-grid { display: grid; gap: 6px; margin-top: 16px; color: #dbeafe; font-size: 0.93rem; }
section { padding: 26px 0 0; border-top: 1px solid var(--line); }
h2 { margin: 0 0 14px; font-size: 1.25rem; line-height: 1.24; letter-spacing: 0; }
h2::after { content: ""; display: block; width: 44px; height: 3px; margin-top: 8px; background: var(--accent); border-radius: 999px; }
.top-list { list-style: none; padding: 0; margin: 0; counter-reset: topitem; display: grid; gap: 12px; }
.news-card {
  counter-increment: topitem;
  position: relative;
  padding: 14px 14px 14px 54px;
  border: 1px solid #d7e3f8;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
}
.news-card::before {
  content: counter(topitem);
  position: absolute;
  left: 14px;
  top: 14px;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 7px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 850;
  font-variant-numeric: tabular-nums;
}
.tag { display: inline-flex; min-height: 24px; padding: 0.1rem 0.48rem; border-radius: 999px; background: #e0f2fe; color: #075985; font-size: 0.75rem; font-weight: 750; }
a { color: #1d4ed8; font-weight: 650; text-decoration: none; border-bottom: 1px solid rgba(37, 99, 235, 0.28); }
.table-wrap { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { width: 100%; border-collapse: collapse; min-width: 560px; font-size: 0.9rem; }
th, td { border: 1px solid var(--line); padding: 0.66rem 0.72rem; text-align: left; vertical-align: top; background: var(--surface); }
th { background: #eef4ff; color: #1e3a8a; font-weight: 800; }
.company-card { border: 1px solid var(--line); border-radius: 8px; background: var(--surface); padding: 14px; margin: 10px 0; }
.warn { margin: 16px 0 0; padding: 0.85rem 1rem; border-left: 4px solid var(--warning-line); border-radius: 0 8px 8px 0; background: var(--warning-bg); color: #7c2d12; }
@media (min-width: 760px) {
  body { padding: 0 28px 58px; }
  .hero-ai { margin-inline: -28px; padding: 42px 28px 24px; }
}
```

## HTML 结构

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YYYY-MM-DD AI 日报</title>
  <style>/* 使用上方 mobile-first UI CSS */</style>
</head>
<body class="report report-ai">
  <header class="hero hero-ai">
    <p class="eyebrow">AI DAILY BRIEF</p>
    <h1>YYYY-MM-DD AI 日报</h1>
    <p class="lead">聚焦新模型、新功能、Agent、开发者工具、算力供给、安全治理与公司动态。</p>
    <div class="meta-grid">生成时间与采集窗口</div>
  </header>
  <section id="window">更新时间与数据窗口</section>
  <section id="top"><h2>今日最重要的 5-10 条</h2><ol class="top-list">...</ol></section>
  <section id="details">分主题详情</section>
  <section id="companies">公司跟踪表或公司卡片</section>
  <section id="risks">风险与不确定性</section>
  <section id="next">明日继续跟踪</section>
  <section id="coverage">来源覆盖与缺口</section>
</body>
</html>
```
