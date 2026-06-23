# Cursor Automation Prompt: 股市日报

你在 `/Users/bobbynie/gitStore/news` 工作。请生成今日股市新闻中文 HTML 日报。

## 日期与时间（必须先执行）

Automation 定时为 **UTC 23:00**（= 澳门次日 **07:00**）。**禁止**直接使用系统注入的 `Today's date`（常为 UTC，会比澳门早一天）。

1. 读取 `automation_trigger_info.triggeredAt`（ISO-8601 UTC）。
2. 换算为 **Asia/Macau (UTC+8)**，得到报告日期 `YYYYMMDD` 与 `YYYY-MM-DD`。
3. 所有路径中的 `YYYYMMDD`、`YYYY-MM`、HTML 标题、commit message 日期，一律用**澳门日历日**。
4. HTML「生成时间」= 上述澳门本地时刻（取自 `triggeredAt`，**禁止**手工编造）。
5. 「采集窗口」= 生成时刻往前 **48 小时** 至生成时刻（澳门时间）。

可运行：`python scripts/report_date.py <TRIGGERED_AT>` 核对日期与窗口。

示例：`2026-05-27T23:02:33.581Z` → 报告日 `20260528`，生成时间 `2026-05-28 07:02（澳门时间）`。

严格按以下步骤执行：

0. **必须先运行** `eval "$(python3 scripts/report_date.py)"`，用输出的 `REPORT_DATE` / `REPORT_ISO` / `REPORT_MONTH` / `REPORT_WINDOW` 作为唯一日期依据。**禁止使用 UTC 或系统默认时区日期**（UTC 23:00 时澳门已是次日）。
1. 读取 `sources/stock-sources.yaml` 和 `sources/source-review-rules.md`。
2. 先重检清单：搜索过去 24-48 小时是否有新的美股/港股重点公司、AI 独角兽、近期 IPO、即将 IPO、SEC/HKEX 披露、官方 IR 来源或主流市场媒体需要加入跟踪。IPO 线索必须优先核对 `ipo_primary_sources`，把结果写入 `tmp/STOCK/YYYYMMDD/00-source-review.md`。
3. 按清单检索 SEC EDGAR、HKEXnews、公司 IR、新闻稿、主流财经媒体和可信市场新闻。把原始发现写入 `tmp/STOCK/YYYYMMDD/01-raw-findings.md`。
4. 去重、按市场影响排序，把候选新闻写入 `tmp/STOCK/YYYYMMDD/02-ranked-items.md`。
5. 生成中文草稿到 `tmp/STOCK/YYYYMMDD/03-draft-cn.md`。
6. **生成 HTML 前**必须完整阅读本文件 **「移动端 UI 设计要求」** 与 **HTML 结构** 章节；以 `2026-06/STOCK/20260602.html` 为结构参考，**禁止**复用 `max-width: 920px` 旧模板。
7. 用中文生成 HTML 报告到 `YYYY-MM/STOCK/YYYYMMDD.html`。报告必须包含：今日最重要 5-10 条、美股重点、港股重点、**港股和美股近期 IPO 专栏**、AI 独角兽/IPO、财报与指引、监管与风险、**事件驱动股票专题**、明日继续跟踪、来源覆盖与缺口。
8. **HTML 生成后**运行 `python3 scripts/validate_report_ui.py --kind STOCK --date YYYYMMDD`，失败则修正后重跑，**通过才可 commit**。
9. 每条重要判断必须附来源链接，价格、涨跌、市值等实时数据必须注明时间和来源。不要给买卖建议。
10. 完成后运行 `python3 scripts/build_pages_index.py` 更新根目录 `index.html`。
11. **必须** `git add`、`git commit`（message: `daily stock news report ${REPORT_ISO}`）。**最终**运行 `./scripts/publish_to_main.sh '<TRIGGERED_AT>'` 合并到 `main` 并 `git push origin main`（禁止只留在 `cursor/*` 分支）。
12. 确认 `main` push 成功；GitHub Actions `Publish News Pages` 会在 push 到 `main` 后自动部署 Pages。备用：仅 push 功能分支时由 `auto-merge-daily.yml` 自动合并。

## 输出要求

- **报告日期与文件名必须使用澳门时区**，且以 `automation_trigger_info.triggeredAt` 换算结果为准（见上文「日期与时间」）。
- 英文来源需翻译成中文并保留原文链接。
- 价格、涨跌、市值、盘前盘后数据必须注明时间、市场和来源。
- 对未上市独角兽只描述融资、估值、IPO、监管和重大商业事件，不做估值建议。
- 不提供买卖建议，只写“可能影响”和“需要继续跟踪”。
- 港股和美股近期 IPO 专栏必须使用 `<section id="recent-ipos">`；没有可验证近期或即将 IPO 时，保留专栏并写明已检查来源、未见足够可靠候选。
- 不得在提示词或来源清单中硬编码固定股票、固定人物或固定公司作为每日必写对象；股票关注必须由当天可核验的公开披露、交易所文件、公司 IR、财报、重大监管/诉讼、异常成交或主流市场媒体共同触发。若某个公司或股票没有窗口内可验证重大变化，不得因为名称预设而写入。

## 港股和美股近期 IPO 专栏要求

股票日报必须固定输出 **港股和美股近期 IPO 专栏**，用于覆盖近 30 日已上市公司和未来 30-60 日即将上市、已递表、已通过聆讯、已提交注册文件或已公布发行区间的公司。重点是分析“是否值得继续关注”，不是给买卖建议。

必须分清两类：

- **近期已上市 IPO**：写上市日期、交易所、发行价、募资规模、首日/近期表现、流通量或锁定期、核心业务、主要风险，价格与涨跌必须注明时间和来源。
- **即将 IPO / 已递表 / 已提交注册文件**：写预计市场、当前阶段、招股书或 SEC S-1/F-1 关键披露、收入增长、毛利率/亏损、现金消耗、客户集中度、行业景气、监管或诉讼风险、发行条款是否已披露。

来源优先级：

- 美股：SEC S-1/F-1、Nasdaq IPO Calendar、NYSE IPO Center、公司 IR/新闻稿；必要时用 Reuters、Bloomberg、FT、Renaissance Capital IPO Center、IPO Scoop 交叉验证。
- 港股：HKEXnews 新申请、聆讯后资料集、招股书、配发结果、公司公告；必要时用 Reuters、Bloomberg、FT、财新、36氪 IPO/资本交叉验证。

每个即将 IPO 的重点候选必须按以下维度做判断：业务质量、财务质量、估值与发行条款、行业景气、基石/战略投资者、流动性与锁定期、监管与诉讼风险。

每家公司必须给出一个非交易建议式的 **关注等级：值得重点关注 / 谨慎关注 / 暂不关注 / 信息不足**，并用 2-3 句解释证据。不得把关注等级写成买入、卖出、目标价或确定收益判断。

## 移动端 UI 设计要求

报告必须是 mobile-first 的单文件 HTML/CSS，适合手机阅读，并呈现真实金融简报感。禁止生成只有默认 `h1/table/ul` 的裸 HTML，也不要做成科技营销页。

- 视觉方向：真实、克制、金融终端/市场简报感；浅色纸面背景，深墨色正文，绿色/红色只用于涨跌与市场状态。
- 页面宽度：`body` 最大宽度约 `780px`，手机左右 padding 约 `18px`，正文 `font-size: 16px` 起、`line-height: 1.65` 左右。
- 首屏：使用 `<header class="hero hero-stock">`，包含英文眉标 `MARKET DAILY BRIEF`、`h1`、一句报告说明、生成时间、采集窗口、市场日历。
- 今日重点：`#top` 内使用 `<ol class="top-list">`，每条为 `<li class="market-card">`，固定写清“事实 -> 可能影响 -> 继续跟踪”，不能给买卖建议。
- 行情数据：价格、涨跌、市值、成交额、盘前盘后必须标注市场、时间和来源；数字使用 `.price` 或 `.quote-line`，CSS 使用 `font-variant-numeric: tabular-nums;`。
- 涨跌表达：上涨用 `.change-up`，下跌用 `.change-down`；颜色只作辅助，文本必须保留 `+` / `-` 与百分比或金额。
- 表格与宽内容：行情表必须包在 `<div class="table-wrap">` 中，允许内部横向滚动，但页面本身不能横向滚动。
- 专题框：如 IPO、财报、监管、重大并购或异常成交专题可用 `.focus-box`，但不要嵌套多层卡片。
- 浏览器自检：生成后用 390px 手机宽度检查 `document.documentElement.scrollWidth <= window.innerWidth`；只有 `.table-wrap` 内部允许横向滚动。
- 语音朗读：必须在 `</header>` 后、正文 section 前加入 `<div class="reader-controls" data-reader-controls>`，包含“朗读 / 暂停 / 继续 / 停止”按钮、语速选择、`⚙` 设置按钮和状态文本；设置点击后必须弹出浮窗，不得把 Google TTS key 直接摊在正文里，控件必须适合 390px 手机宽度且不得造成页面横向滚动。
- 朗读脚本：必须引用共用 JS `<script src="../../assets/report-reader.js" defer></script>`，不要重新生成或改写朗读逻辑；共用 JS 会只朗读正文、优先使用用户本机保存的 Google TTS key、失败时回退浏览器普通话朗读。
- Google TTS 设置：设置窗必须使用 `<dialog class="reader-settings" data-reader-settings>`；控件必须包含 `data-reader-settings-open`、`data-reader-settings-close`、`data-google-tts-key`、`data-google-tts-voice`、`data-google-tts-save`、`data-google-tts-clear`；提示用户 API key 只保存在本机 `localStorage`，并应在 Google Cloud 限制 Text-to-Speech API 与 HTTP referrer。
- 所有 CSS 必须内联在 `<style>`；JS 只引用本仓库 `assets/report-reader.js`，不内联朗读逻辑，不依赖外部 JS 或远程字体。

建议使用以下视觉基底，可按内容轻微调整但必须保留类名：

```css
:root {
  --paper: #f7f6f0;
  --ink: #111827;
  --muted: #6b7280;
  --line: #d8d2c3;
  --surface: #fffefa;
  --market: #14532d;
  --up: #087443;
  --down: #b42318;
  --blue: #1d4ed8;
  --warning-bg: #fff7ed;
  --warning-line: #ea580c;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0 auto;
  max-width: 780px;
  min-height: 100vh;
  padding: 0 18px 46px;
  background: linear-gradient(180deg, #efeadf 0, rgba(239, 234, 223, 0) 330px), var(--paper);
  color: var(--ink);
  font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", sans-serif;
  font-size: 16px;
  line-height: 1.66;
  letter-spacing: 0;
}
.hero-stock {
  margin: 0 -18px;
  padding: 28px 18px 18px;
  color: #101828;
  background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(255,255,255,0.62)), #efe8d8;
  border-bottom: 1px solid var(--line);
}
.eyebrow {
  margin: 0 0 12px;
  color: var(--market);
  font-size: 0.74rem;
  font-weight: 850;
  letter-spacing: 0.12em;
}
h1 { margin: 0; font-size: clamp(1.75rem, 8vw, 2.32rem); line-height: 1.12; letter-spacing: 0; }
.lead { margin: 12px 0 0; color: #374151; }
.market-strip { display: grid; gap: 6px; margin-top: 16px; color: var(--muted); font-size: 0.93rem; }
section { margin: 0; padding: 26px 0 0; border-top: 1px solid var(--line); }
h2 { margin: 0 0 14px; color: #172554; font-size: 1.22rem; line-height: 1.25; letter-spacing: 0; }
h2::after { content: ""; display: block; width: 48px; height: 3px; margin-top: 8px; background: var(--market); border-radius: 999px; }
.top-list { list-style: none; padding: 0; margin: 0; counter-reset: marketitem; display: grid; gap: 12px; }
.market-card {
  counter-increment: marketitem;
  position: relative;
  padding: 14px 14px 14px 54px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 8px 22px rgba(74, 63, 38, 0.06);
}
.market-card::before {
  content: counter(marketitem);
  position: absolute;
  left: 14px;
  top: 14px;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 6px;
  background: #dcfce7;
  color: var(--market);
  font-weight: 850;
  font-variant-numeric: tabular-nums;
}
.quote-line, .price, .change-up, .change-down, td:nth-child(2), td:nth-child(3) {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;
}
.change-up { color: var(--up); font-weight: 850; }
.change-down { color: var(--down); font-weight: 850; }
a { color: var(--blue); font-weight: 650; text-decoration: none; border-bottom: 1px solid rgba(29, 78, 216, 0.28); }
.table-wrap { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { width: 100%; border-collapse: collapse; min-width: 620px; font-size: 0.9rem; }
th, td { border: 1px solid var(--line); padding: 0.64rem 0.72rem; text-align: left; vertical-align: top; background: var(--surface); }
th { background: #eee7d7; color: #374151; font-weight: 850; }
.focus-box { margin: 14px 0 0; padding: 16px; border: 1px solid #c7d2fe; border-radius: 8px; background: #f8fbff; }
.warn { margin: 14px 0 0; padding: 0.85rem 1rem; border-left: 4px solid var(--warning-line); border-radius: 0 8px 8px 0; background: var(--warning-bg); color: #7c2d12; }
.reader-controls { margin: 16px 0 0; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
.reader-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.reader-controls button, .reader-controls select, .reader-controls input { min-height: 40px; border: 1px solid #cbbf9f; border-radius: 7px; background: #ffffff; color: #1f2937; font: inherit; }
.reader-controls button { padding: 0 0.72rem; font-weight: 750; }
.reader-controls select, .reader-controls input { padding: 0 0.5rem; max-width: 100%; }
.reader-settings-toggle { width: 40px; padding: 0; display: grid; place-items: center; font-size: 1rem; }
.reader-settings { border: 0; padding: 0; background: transparent; }
.reader-settings::backdrop { background: rgba(15, 23, 42, 0.38); }
.reader-settings-panel { width: min(360px, calc(100vw - 24px)); padding: 14px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); box-shadow: 0 22px 60px rgba(15, 23, 42, 0.28); }
.reader-settings-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 10px; }
.reader-settings-grid { display: grid; gap: 10px; }
.reader-settings-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.reader-settings-note { margin: 8px 0 0; color: var(--muted); font-size: 0.88rem; }
.reader-status { margin: 8px 0 0; color: var(--muted); font-size: 0.9rem; }
@media (min-width: 760px) {
  body { padding: 0 28px 58px; }
  .hero-stock { margin-inline: -28px; padding: 42px 28px 24px; }
}
```

## HTML 结构

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YYYY-MM-DD 股市日报</title>
  <style>/* 使用上方 mobile-first UI CSS */</style>
</head>
<body class="report report-stock">
  <header class="hero hero-stock">
    <p class="eyebrow">MARKET DAILY BRIEF</p>
    <h1>YYYY-MM-DD 股市日报</h1>
    <p class="lead">美股、港股、近期 IPO、AI IPO、财报与监管风险。</p>
    <div class="market-strip">生成时间、采集窗口与市场日历</div>
  </header>
  <div class="reader-controls" data-reader-controls>
    <div class="reader-actions">
      <button type="button" data-reader-start>朗读</button>
      <button type="button" data-reader-pause>暂停</button>
      <button type="button" data-reader-resume>继续</button>
      <button type="button" data-reader-stop>停止</button>
      <label>语速 <select data-reader-rate><option value="0.8">0.8x</option><option value="1" selected>1.0x</option><option value="1.2">1.2x</option></select></label>
      <button type="button" class="reader-settings-toggle" data-reader-settings-open aria-label="设置" title="设置">⚙</button>
    </div>
    <dialog class="reader-settings" data-reader-settings aria-label="朗读设置">
      <div class="reader-settings-panel">
        <div class="reader-settings-head">
          <strong>朗读设置</strong>
          <button type="button" data-reader-settings-close aria-label="关闭">×</button>
        </div>
        <div class="reader-settings-grid">
          <label>Google TTS Key <input type="password" data-google-tts-key autocomplete="off" placeholder="可选，本机保存"></label>
          <label>Google 音色 <select data-google-tts-voice><option value="cmn-CN-Wavenet-A" selected>cmn-CN-Wavenet-A</option><option value="cmn-CN-Wavenet-B">cmn-CN-Wavenet-B</option><option value="cmn-CN-Wavenet-C">cmn-CN-Wavenet-C</option><option value="cmn-CN-Wavenet-D">cmn-CN-Wavenet-D</option></select></label>
        </div>
        <div class="reader-settings-actions">
          <button type="button" data-google-tts-save>保存 Key</button>
          <button type="button" data-google-tts-clear>清除 Key</button>
        </div>
        <p class="reader-settings-note">API key 只保存在本机 <code>localStorage</code>，请在 Google Cloud 限制 Text-to-Speech API 与 HTTP referrer。</p>
      </div>
    </dialog>
    <p class="reader-status" data-reader-status>可使用浏览器语音朗读本文；若保存 Google TTS key，会优先使用 Google 云端普通话朗读。</p>
  </div>
  <section id="window">更新时间与数据窗口</section>
  <section id="top"><h2>今日最重要的 5-10 条</h2><ol class="top-list">...</ol></section>
  <section id="us">美股重点</section>
  <section id="hk">港股重点</section>
  <section id="recent-ipos"><h2>港股和美股近期 IPO 专栏</h2></section>
  <section id="unicorns">AI 独角兽 / IPO</section>
  <section id="earnings">财报与指引</section>
  <section id="risks">监管与风险</section>
  <section id="event-focus">事件驱动股票专题</section>
  <section id="next">明日继续跟踪</section>
  <section id="coverage">来源覆盖与缺口</section>
  <script src="../../assets/report-reader.js" defer></script>
</body>
</html>
```
