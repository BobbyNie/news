# Cursor Automation Prompt: 每日 AI + 股市双日报（合并 Cron）

适用于 **一条** Cursor Automation Cron 任务同时生成 AI 与股市两份 HTML 日报（例如 `0 23 * * *` UTC = 澳门次日 07:00）。

## 0. 必须先读的文件（禁止跳过）

生成任何 HTML **之前**，必须完整读取：

1. `prompts/cursor-ai-daily.md` — 尤其 **「移动端 UI 设计要求」** 与 **HTML 结构** 章节
2. `prompts/cursor-stock-daily.md` — 尤其 **「移动端 UI 设计要求」** 与 **HTML 结构** 章节
3. `sources/source-review-rules.md`
4. `sources/ai-sources.yaml` / `sources/stock-sources.yaml`

**禁止**复用 `2026-05/*` 或 `max-width: 920px` 的旧裸 HTML 模板。正确参考：`2026-06/AI/20260602.html`、`2026-06/STOCK/20260602.html`。

## 1. 日期与时间（必须先执行）

1. 读取 `automation_trigger_info.triggeredAt`（ISO-8601 UTC）。
2. 运行：`eval "$(python3 scripts/report_date.py '<TRIGGERED_AT>')"`
3. 全程使用 `$REPORT_DATE` / `$REPORT_ISO` / `$REPORT_MONTH` / `$REPORT_GENERATED_AT` / `$REPORT_WINDOW`。
4. **禁止**使用系统注入的 `Today's date`（UTC 会比澳门早一天）。

## 2. AI 日报流程

按 `prompts/cursor-ai-daily.md` 执行步骤 1–8（来源重检 → 原始发现 → 排序 → HTML）。

HTML 必须包含（CI 会校验）：

- `AI DAILY BRIEF`、`hero hero-ai`、`top-list`、`news-card`、`table-wrap`
- `body { max-width: 760px; }`、`-webkit-text-size-adjust: 100%`
- **不得**出现 `max-width: 920px`

输出：`tmp/AI/$REPORT_DATE/`、`$REPORT_MONTH/AI/$REPORT_DATE.html`

生成后 **必须**运行并通过：

```bash
python3 scripts/validate_report_ui.py --kind AI --date "$REPORT_DATE"
```

## 3. 股市日报流程

按 `prompts/cursor-stock-daily.md` 执行；须含 **马斯克相关股票专题**。

HTML 必须包含（CI 会校验）：

- `MARKET DAILY BRIEF`、`hero hero-stock`、`top-list`、`market-card`、`change-up`、`table-wrap`
- `body { max-width: 780px; }`、`-webkit-text-size-adjust: 100%`
- **不得**出现 `max-width: 920px`

输出：`tmp/STOCK/$REPORT_DATE/`、`$REPORT_MONTH/STOCK/$REPORT_DATE.html`

生成后 **必须**运行并通过：

```bash
python3 scripts/validate_report_ui.py --kind STOCK --date "$REPORT_DATE"
```

## 4. 发布前门禁（全部通过才可 push）

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -q
python3 scripts/validate_report_ui.py --kind AI --date "$REPORT_DATE"
python3 scripts/validate_report_ui.py --kind STOCK --date "$REPORT_DATE"
python3 scripts/build_pages_index.py
git add ...
git commit -m "daily AI news report $REPORT_ISO"    # AI 变更
git commit -m "daily stock news report $REPORT_ISO" # 股市变更（可分开）
git push origin main
```

若 `validate_report_ui.py` 失败：**不得 push**；应修正 HTML 直至通过，或对照 `2026-06/*20260602.html` 迁移样式。

## 5. 移动端 UI 快速自检清单

| 检查项 | AI | 股市 |
|--------|----|------|
| 首屏 hero | `hero-ai` + 深色顶栏 | `hero-stock` + 纸面顶栏 |
| 要闻列表 | `ol.top-list` > `li.news-card` | `ol.top-list` > `li.market-card` |
| 表格 | 包在 `div.table-wrap` 内 | 同上 |
| 页宽 | 760px | 780px |
| 涨跌色 | — | `.change-up` / `.change-down` |
| 390px 视口 | 页面本身不横向滚动 | 同上 |

Commit message 示例：`daily AI news report YYYY-MM-DD`、`daily stock news report YYYY-MM-DD`。
