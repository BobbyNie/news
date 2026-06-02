# AI 和股市 News

**在线阅读（GitHub Pages）：** https://bobbynie.github.io/news/

这是一个由 Cursor Automation 驱动的每日新闻汇报仓库。项目不依赖采集脚本，核心流程由两条自动化任务完成：

- AI 日报：跟踪全球 AI 公司、官方发布、主流媒体、论坛和研究社区。
- 股市日报：跟踪美股、港股重点公司，AI 独角兽、IPO、财报、监管和重大市场新闻。

## 目录结构

```text
sources/
  ai-sources.yaml
  stock-sources.yaml
  source-review-rules.md
prompts/
  cursor-ai-daily.md
  cursor-stock-daily.md
tmp/
  AI/YYYYMMDD/
  STOCK/YYYYMMDD/
YYYY-MM/
  AI/YYYYMMDD.html
  STOCK/YYYYMMDD.html
archive/
  rejected/
```

## 每日流程

1. 读取对应来源清单。
2. 先重检来源清单，记录新增建议和失效来源。
3. 检索官方公告、RSS、公司 IR、交易所披露、主流媒体、X/Facebook 补充消息、论坛和研究社区。
4. 将原始发现写入 `tmp/<AI|STOCK>/YYYYMMDD/01-raw-findings.md`。
5. 去重、排序并生成中文 HTML 日报。
6. 输出到 `YYYY-MM/AI/YYYYMMDD.html` 或 `YYYY-MM/STOCK/YYYYMMDD.html`。
7. 运行 `python3 scripts/build_pages_index.py` 更新索引。
8. `git commit` 并 **`git push origin main`**（Pages 仅在有 push 时发布）。

## 报告日期（澳门时区）

Automation Cron 若为 `0 23 * * *`（UTC），触发时刻 = **澳门次日 07:00**。报告日期必须以 **`automation_trigger_info.triggeredAt`** 换算 Asia/Macau，**禁止**使用系统注入的 UTC「今天」。

生成前可核对：

```bash
python3 scripts/report_date.py 2026-05-27T23:02:33.581Z
# 或本地当前澳门时刻（publish 脚本用）：
eval "$(python3 scripts/report_date.py)"
echo "$REPORT_DATE $REPORT_ISO $REPORT_GENERATED_AT"
```

所有 `tmp/`、`YYYY-MM/` 路径与 HTML 标题必须使用上述日期。HTML「生成时间」= `$REPORT_GENERATED_AT` 或 `triggeredAt` 换算结果，**禁止手工编造**。

## 自动化任务

建议在 Cursor Automation 中创建任务（Cron 示例 `0 23 * * *` = **UTC 23:00 = 澳门次日 07:00**）：

- **合并双日报（推荐）**：使用 [prompts/cursor-automation-combined.md](prompts/cursor-automation-combined.md) — 一条 Cron 同时生成 AI + 股市，并强制 mobile-first UI 校验。
- AI 日报：使用 [prompts/cursor-ai-daily.md](prompts/cursor-ai-daily.md)。
- 股市日报：使用 [prompts/cursor-stock-daily.md](prompts/cursor-stock-daily.md)。

生成 HTML 后 **必须**通过 UI 校验（否则 CI 会失败、不得 push）：

```bash
python3 scripts/validate_report_ui.py --kind AI --date "$REPORT_DATE"
python3 scripts/validate_report_ui.py --kind STOCK --date "$REPORT_DATE"
# 或批量校验 2026-06-01 起的全部报告：
python3 scripts/validate_report_ui.py --all-since 20260601
```

也可改用 Cron `0 8 * * *` + 时区 `Asia/Macau`，则 `triggeredAt` 与澳门日历日一致，逻辑相同。

两条任务完成后都必须 **push 到 `main`**，否则 GitHub 上看不到新提交，Pages 也不会更新。

## GitHub Pages 发布

每次提交到 `main` 后，GitHub Actions 会自动：

1. [validate-reports.yml](.github/workflows/validate-reports.yml)：运行全部单元测试 + `validate_report_ui.py --all-since 20260601`。
2. [pages.yml](.github/workflows/pages.yml)：同上校验通过后构建并部署 Pages。
3. 扫描 `YYYY-MM/AI/*.html` 和 `YYYY-MM/STOCK/*.html`，生成最新报告在最上面的 `index.html`。

本地预览索引可运行：

```bash
python3 scripts/build_pages_index.py
```

生成 Pages 发布目录可运行：

```bash
python3 scripts/build_pages_index.py --site-dir public
```

## 来源策略

采用“公开优先”策略：

- 官方博客、RSS、公司 IR、SEC EDGAR、HKEXnews、主流媒体优先。
- X/Facebook 只作为补充来源，必须验证官方账号。
- 无法访问或无法验证的消息必须在报告中标注为缺口或待确认。
- 报告不提供买卖建议，只描述可能影响和后续观察点。
