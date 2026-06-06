# Cursor Automation Prompt: AI + 股市周报

你在 `/Users/bobbynie/gitStore/news` 工作。请在每周日的 automation 运行时，生成本周 AI + 股市中文 HTML 周报。

## 日期、周次与输出路径（必须先执行）

1. 读取 `automation_trigger_info.triggeredAt`（ISO-8601 UTC）。
2. 运行：

```bash
eval "$(python3 scripts/report_date.py '<TRIGGERED_AT>')"
```

3. 全程使用脚本输出的 `REPORT_GENERATED_AT`、`REPORT_WEEK_START`、`REPORT_WEEK_END`、`REPORT_WEEK_MONTH`、`REPORT_WEEK_FILE`、`REPORT_WEEK_LABEL`、`REPORT_WEEK_WINDOW`。
4. 周报截止日 = `triggeredAt` 换算到 **Asia/Macau** 后最近一个已经结束的周日；若 automation 设为 UTC 周日 23:00，澳门已是周一 07:00，仍应生成刚结束的周日周报。
5. 输出 HTML 到 `${REPORT_WEEK_MONTH}/${REPORT_WEEK_FILE}.html`，文件名格式为 `YYYY-Www.html`，例如 `2026-06/2026-W23.html`。
6. 发布 URL 为 `https://bobbynie.github.io/news/${REPORT_WEEK_MONTH}/${REPORT_WEEK_FILE}.html`。

严格按以下步骤执行：

0. **必须先运行**上方 `report_date.py` 命令，禁止使用系统默认日期或 UTC 的 `Today's date`。
1. **生成 HTML 前必须完整阅读**：
   - `prompts/cursor-ai-daily.md` 的「AI 行业内容边界」、「移动端 UI 设计要求」与「HTML 结构」
   - `prompts/cursor-stock-daily.md` 的「移动端 UI 设计要求」与「HTML 结构」
   - `sources/source-review-rules.md`
   - `sources/ai-sources.yaml` / `sources/stock-sources.yaml`
2. 先做来源重检，记录本周新增、失效或需要调整的来源，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/00-source-review.md`。
3. 检索 `REPORT_WEEK_WINDOW` 内的 AI 行业进展，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/01-ai-findings.md`。必须遵守 AI 行业内容边界：优先新模型、新功能、Agent、开发者工具/API、开源/研究、企业采用、算力供给、安全/治理与公司产品路线；不得用宏观、股价、指数、IPO 定价或资金流填充 AI 主线。
4. 检索 `REPORT_WEEK_WINDOW` 内的美股、港股、AI IPO/独角兽、财报指引、监管风险、重要公司新闻与马斯克相关股票专题，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/02-stock-findings.md`。
5. 去重并按“本周影响力”和“下周可继续跟踪性”排序，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/03-ranked-weekly-themes.md`。同一事件若同时影响 AI 行业与股市，只保留一个主条目，并在影响分析中分别写清 AI 与市场维度。
6. 生成中文草稿到 `tmp/WEEKLY/${REPORT_WEEK_FILE}/04-draft-cn.md`。
7. 用中文生成 HTML 周报到 `${REPORT_WEEK_MONTH}/${REPORT_WEEK_FILE}.html`。标题使用 `${REPORT_WEEK_LABEL} AI + 股市周报`。
8. 生成后运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -q
python3 scripts/validate_report_ui.py --latest
python3 scripts/build_pages_index.py
```

9. 确认根目录 `index.html` 已出现本周周报链接。
10. 提交并发布。推荐直接运行：

```bash
./scripts/publish_to_main.sh --weekly '<TRIGGERED_AT>'
```

若不能运行 publish 脚本，必须至少 `git add tmp/WEEKLY/${REPORT_WEEK_FILE}/ ${REPORT_WEEK_MONTH}/${REPORT_WEEK_FILE}.html index.html`，再 `git commit -m "weekly AI stock news report ${REPORT_WEEK_FILE}"`，并确保变更进入 `main` 后触发 Pages。

## 输出要求

- 周报必须覆盖 `REPORT_WEEK_WINDOW`，不是单日日报拼接。
- 每条重要判断必须附可点击来源链接；英文来源需翻译成中文并保留原文链接。
- AI 内容遵守 `cursor-ai-daily.md` 的 **AI 行业内容边界**，股市内容遵守 `cursor-stock-daily.md` 的市场数据与风险表达要求。
- 价格、涨跌、市值、成交额、盘前盘后数据必须注明市场、时间和来源。
- 不提供买卖建议，只写事实、可能影响、风险与下周继续跟踪点。
- 无法访问或无法验证的来源要在“来源覆盖与缺口”列出。

## 周报结构

HTML 必须包含：

1. 首屏：`<header class="hero hero-weekly">`，英文眉标 `AI + MARKET WEEKLY BRIEF`，标题 `${REPORT_WEEK_LABEL} AI + 股市周报`，生成时间、周报窗口、输出 URL。
2. `#top`：本周最重要 8-12 条，使用 `<ol class="top-list">` 与 `<li class="weekly-card">`。每条写清“事实 -> AI 影响 -> 市场影响 -> 下周跟踪”。
3. `#ai`：AI 行业主线，覆盖模型/产品/Agent/开发者工具/算力/安全治理。
4. `#market`：股市主线，覆盖美股、港股、AI IPO/独角兽、财报与监管。
5. `#cross-impact`：AI 与股市交叉影响，说明产品、算力、监管、财报或资本市场事件如何互相反馈。
6. `#finance-ai-applications`：金融业 AI 应用专栏（银行优先），无可验证更新时写明已检查来源与缺口。
7. `#musk`：与伊隆·马斯克相关的股票专题。
8. `#risks`：风险与不确定性。
9. `#next`：下周继续跟踪。
10. `#coverage`：来源覆盖与缺口。

## 移动端 UI 设计要求

周报必须是 mobile-first 的单文件 HTML/CSS，适合手机阅读。必须参考 AI 日报和股市日报的「移动端 UI 设计要求」，但周报要呈现一页综合周报，不要做成两份日报的复制粘贴。

- 视觉方向：克制的研究周报感，浅色正文背景，首屏深色标题区，蓝色用于 AI 线索，绿色/红色只用于市场涨跌状态。
- 页面宽度：`body` 最大宽度约 `800px`，手机左右 padding 约 `18px`，正文 `font-size: 16px` 起、`line-height: 1.65` 左右。
- 不得使用 `max-width: 920px` 旧模板，不得生成裸 `h1/table/ul` 页面。
- 所有 CSS 必须内联在 `<style>`，不依赖外部字体、JS 或远程资源。
- 表格必须包在 `<div class="table-wrap">` 中允许内部横向滚动；页面本身不得横向滚动。
- 浏览器自检：用 390px 手机宽度检查 `document.documentElement.scrollWidth <= window.innerWidth`，只有 `.table-wrap` 内部允许横向滚动。

建议使用以下视觉基底，可按内容轻微调整但必须保留类名：

```css
:root {
  --paper: #f6f8fb;
  --ink: #111827;
  --muted: #667085;
  --line: #d9e2ef;
  --surface: #ffffff;
  --ai: #2563eb;
  --market: #14532d;
  --up: #087443;
  --down: #b42318;
  --warning-bg: #fff7ed;
  --warning-line: #ea580c;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0 auto;
  max-width: 800px;
  min-height: 100vh;
  padding: 0 18px 46px;
  background: linear-gradient(180deg, #eaf1ff 0, rgba(234, 241, 255, 0) 340px), var(--paper);
  color: var(--ink);
  font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", sans-serif;
  font-size: 16px;
  line-height: 1.66;
  letter-spacing: 0;
}
.hero-weekly {
  margin: 0 -18px;
  padding: 30px 18px 20px;
  background: #101828;
  color: #f8fafc;
  border-bottom: 4px solid var(--ai);
}
.eyebrow { margin: 0 0 12px; color: #93c5fd; font-size: 0.74rem; font-weight: 850; letter-spacing: 0.12em; }
h1 { margin: 0; font-size: clamp(1.76rem, 8vw, 2.42rem); line-height: 1.12; letter-spacing: 0; }
.lead { margin: 12px 0 0; color: #dbeafe; }
.meta-grid { display: grid; gap: 6px; margin-top: 16px; color: #dbeafe; font-size: 0.93rem; }
section { margin: 0; padding: 26px 0 0; border-top: 1px solid var(--line); }
h2 { margin: 0 0 14px; font-size: 1.24rem; line-height: 1.25; letter-spacing: 0; }
h2::after { content: ""; display: block; width: 48px; height: 3px; margin-top: 8px; background: var(--ai); border-radius: 999px; }
.top-list { list-style: none; padding: 0; margin: 0; counter-reset: weeklyitem; display: grid; gap: 12px; }
.weekly-card {
  counter-increment: weeklyitem;
  position: relative;
  padding: 14px 14px 14px 54px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
}
.weekly-card::before {
  content: counter(weeklyitem);
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
.quote-line, .price, .change-up, .change-down { font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }
.change-up { color: var(--up); font-weight: 850; }
.change-down { color: var(--down); font-weight: 850; }
a { color: #1d4ed8; font-weight: 650; text-decoration: none; border-bottom: 1px solid rgba(29, 78, 216, 0.28); }
.table-wrap { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { width: 100%; border-collapse: collapse; min-width: 620px; font-size: 0.9rem; }
th, td { border: 1px solid var(--line); padding: 0.64rem 0.72rem; text-align: left; vertical-align: top; background: var(--surface); }
th { background: #eef4ff; color: #1e3a8a; font-weight: 850; }
.focus-box { margin: 14px 0 0; padding: 16px; border: 1px solid #c7d2fe; border-radius: 8px; background: #f8fbff; }
.warn { margin: 14px 0 0; padding: 0.85rem 1rem; border-left: 4px solid var(--warning-line); border-radius: 0 8px 8px 0; background: var(--warning-bg); color: #7c2d12; }
@media (min-width: 760px) {
  body { padding: 0 28px 58px; }
  .hero-weekly { margin-inline: -28px; padding: 42px 28px 24px; }
}
```

## HTML 结构

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>REPORT_WEEK_LABEL AI + 股市周报</title>
  <style>/* 使用上方 mobile-first UI CSS */</style>
</head>
<body class="report report-weekly">
  <header class="hero hero-weekly">
    <p class="eyebrow">AI + MARKET WEEKLY BRIEF</p>
    <h1>REPORT_WEEK_LABEL AI + 股市周报</h1>
    <p class="lead">综合本周 AI 行业进展、市场变化、财报/IPO、监管风险与下周观察。</p>
    <div class="meta-grid">生成时间、周报窗口、发布 URL</div>
  </header>
  <section id="window">更新时间与周报窗口</section>
  <section id="top"><h2>本周最重要的 8-12 条</h2><ol class="top-list">...</ol></section>
  <section id="ai">AI 行业主线</section>
  <section id="market">股市主线</section>
  <section id="cross-impact">AI 与股市交叉影响</section>
  <section id="finance-ai-applications">金融业 AI 应用专栏（银行优先）</section>
  <section id="musk">马斯克相关股票专题</section>
  <section id="risks">风险与不确定性</section>
  <section id="next">下周继续跟踪</section>
  <section id="coverage">来源覆盖与缺口</section>
</body>
</html>
```
