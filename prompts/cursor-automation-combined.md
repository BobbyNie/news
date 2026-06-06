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

必须遵守 `prompts/cursor-ai-daily.md` 的 **AI 行业内容边界**：AI 日报聚焦新模型、新功能、Agent、开发者工具/API、开源/研究、企业或行业 AI 采用、算力供给、安全/治理和公司产品路线。

不得把宏观、利率、股价、指数、IPO 定价或入指事件作为 AI 日报主线；只有直接改变 AI 产品路线、模型能力、算力供给或企业采用时，才可作为低优先级背景。纯股票、指数、估值、募资规模、资金流与交易风险写入股市日报，不要写入 AI 日报。

AI HTML 必须在下方固定包含 `<section id="finance-ai-applications">`，标题为「金融业 AI 应用专栏（银行优先）」：只写银行、券商、保险、资管、支付、交易所、监管科技等主体如何应用或建设 AI，尤其是银行新服务、客户服务、财富管理、风控/反欺诈、信贷审批、合规/监管科技、内部开发者工具、AI 基础设施建设、模型治理或与 AI 公司/云厂商共建项目。不得用宏观、利率、股价、指数、IPO 定价、入指事件、金融就业或券商观点填充。

HTML 必须包含（CI 会校验）：

- `AI DAILY BRIEF`、`hero hero-ai`、`top-list`、`news-card`、`table-wrap`、`finance-ai-applications`
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

## 4. 发布前门禁（全部通过才可上线）

**禁止**只 `git push` 到 `cursor/*` 功能分支就结束。GitHub Pages **仅**在 `main` 有 push 时部署（见 `.github/workflows/pages.yml`）。

### 4.1 在功能分支上先提交日报（可分开两次 commit）

```bash
# 已 eval report_date.py，且 $REPORT_DATE 等变量已就绪
git add tmp/AI/$REPORT_DATE/ $REPORT_MONTH/AI/$REPORT_DATE.html
git commit -m "daily AI news report $REPORT_ISO"

git add tmp/STOCK/$REPORT_DATE/ $REPORT_MONTH/STOCK/$REPORT_DATE.html
git commit -m "daily stock news report $REPORT_ISO"
```

### 4.2 合并到 main 并触发 Pages（必须执行）

将 `<TRIGGERED_AT>` 替换为 `automation_trigger_info.triggeredAt`：

```bash
chmod +x scripts/publish_to_main.sh
./scripts/publish_to_main.sh '<TRIGGERED_AT>'
```

脚本会：跑全套测试与 `validate_report_ui.py` → `build_pages_index.py` → 若当前不在 `main` 则 **merge 进 main** → `git push origin main`。

若 Agent 环境无法执行上述脚本，至少 `git push origin <当前分支>`；仓库已配置 `.github/workflows/auto-merge-daily.yml`，在检测到 `YYYY-MM/(AI|STOCK)/YYYYMMDD.html` 推送至 `cursor/**` 时会 **自动合并到 main**（备用路径，可能延迟数分钟）。

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
