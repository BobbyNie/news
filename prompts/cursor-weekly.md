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
3. **先读取本周已生成的每日 AI 日报与股市日报**，把日报已覆盖事实、来源、缺口和连续主题整合成周报基线，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/01-daily-report-rollup.md`。
   - 遍历 `REPORT_WEEK_START` 到 `REPORT_WEEK_END` 的每个澳门日历日 `YYYYMMDD`。
   - 读取 `${REPORT_WEEK_MONTH}/AI/YYYYMMDD.html` 与 `${REPORT_WEEK_MONTH}/STOCK/YYYYMMDD.html`（若跨月，也检查对应日期自己的 `YYYY-MM/AI/YYYYMMDD.html` 与 `YYYY-MM/STOCK/YYYYMMDD.html`）。
   - 同时读取 `tmp/AI/YYYYMMDD/02-ranked-items.md`、`tmp/AI/YYYYMMDD/03-draft-cn.md`、`tmp/STOCK/YYYYMMDD/02-ranked-items.md`、`tmp/STOCK/YYYYMMDD/03-draft-cn.md`。
   - 若某天日報或 tmp artifact 缺失，在 rollup 中记录缺口；不得跳过既有日報只重新检索，也不得把日報已经覆盖过的事实当成本周新发现重复堆叠。
4. 检索 `REPORT_WEEK_WINDOW` 内的 AI 行业进展，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/02-ai-findings.md`。必须以 `01-daily-report-rollup.md` 为基线，只补充、核验或更新日報未覆盖/后续有变化的事实。必须遵守 AI 行业内容边界：优先新模型、新功能、Agent、开发者工具/API、开源/研究、企业采用、算力供给、安全/治理与公司产品路线；不得用宏观、股价、指数、IPO 定价或资金流填充 AI 主线。
5. 检索 `REPORT_WEEK_WINDOW` 内的美股、港股、AI IPO/独角兽、财报指引、监管风险、重要公司新闻与马斯克相关股票专题，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/03-stock-findings.md`。必须以 `01-daily-report-rollup.md` 为基线，只补充、核验或更新日報未覆盖/后续有变化的事实。
6. 去重并按“本周影响力”和“下周可继续跟踪性”排序，写入 `tmp/WEEKLY/${REPORT_WEEK_FILE}/04-ranked-weekly-themes.md`。同一事件若同时影响 AI 行业与股市，只保留一个主条目，并在影响分析中分别写清 AI 与市场维度。
7. 生成中文草稿到 `tmp/WEEKLY/${REPORT_WEEK_FILE}/05-draft-cn.md`。
8. 用中文生成 HTML 周报到 `${REPORT_WEEK_MONTH}/${REPORT_WEEK_FILE}.html`。标题使用 `${REPORT_WEEK_LABEL} AI + 股市周报`。
9. 生成后运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -q
python3 scripts/validate_report_ui.py --latest
python3 scripts/build_pages_index.py
```

10. 确认根目录 `index.html` 已出现本周周报链接。
11. 提交并发布。推荐直接运行：

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
2. 语音朗读：`</header>` 后必须加入 `<div class="reader-controls" data-reader-controls>`，包含“朗读 / 暂停 / 继续 / 停止”按钮、语速选择、`⚙` 设置按钮和状态文本；设置点击后必须弹出浮窗，并在文末引用共用 JS `<script src="../assets/report-reader.js" defer></script>`；不要重新生成或改写朗读逻辑。
3. `#top`：本周最重要 8-12 条，使用 `<ol class="top-list">` 与 `<li class="weekly-card">`。每条写清“事实 -> AI 影响 -> 市场影响 -> 下周跟踪”。
4. `#ai`：AI 行业主线，覆盖模型/产品/Agent/开发者工具/算力/安全治理。
5. `#market`：股市主线，覆盖美股、港股、AI IPO/独角兽、财报与监管。
6. `#cross-impact`：AI 与股市交叉影响，说明产品、算力、监管、财报或资本市场事件如何互相反馈。
7. `#finance-ai-applications`：金融业 AI 应用专栏（银行优先），无可验证更新时写明已检查来源与缺口。
8. `#musk`：与伊隆·马斯克相关的股票专题。
9. `#risks`：风险与不确定性。
10. `#next`：下周继续跟踪。
11. `#coverage`：来源覆盖与缺口。

## 移动端 UI 设计要求

周报必须是 mobile-first 的单文件 HTML/CSS，适合手机阅读。必须参考 AI 日报和股市日报的「移动端 UI 设计要求」，但周报要呈现一页综合周报，不要做成两份日报的复制粘贴。

- 视觉方向：克制的研究周报感，浅色正文背景，首屏深色标题区，蓝色用于 AI 线索，绿色/红色只用于市场涨跌状态。
- 页面宽度：`body` 最大宽度约 `800px`，手机左右 padding 约 `18px`，正文 `font-size: 16px` 起、`line-height: 1.65` 左右。
- 不得使用 `max-width: 920px` 旧模板，不得生成裸 `h1/table/ul` 页面。
- 语音朗读控件必须适合 390px 手机宽度，不得造成页面横向滚动；设置窗必须使用 `<dialog class="reader-settings" data-reader-settings>`；必须包含 `data-reader-settings-open`、`data-reader-settings-close`、`data-google-tts-key`、`data-google-tts-voice`、`data-google-tts-save`、`data-google-tts-clear`；提示用户 API key 只保存在本机 `localStorage`，并应在 Google Cloud 限制 Text-to-Speech API 与 HTTP referrer。
- 朗读逻辑必须只引用共用 JS，不内联；共用 JS 会只朗读正文、优先使用用户本机保存的 Google TTS key、失败时回退浏览器普通话朗读。
- 所有 CSS 必须内联在 `<style>`；JS 只引用本仓库 `assets/report-reader.js`，不依赖外部 JS 或远程字体。
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
.reader-controls { margin: 16px 0 0; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: rgba(255,255,255,0.94); }
.reader-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.reader-controls button, .reader-controls select, .reader-controls input { min-height: 40px; border: 1px solid #c7d2fe; border-radius: 7px; background: #ffffff; color: #1f2937; font: inherit; }
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
  <script src="../assets/report-reader.js" defer></script>
</body>
</html>
```
