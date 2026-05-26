# AI 和股市 News

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
7. 检查变更并提交 git。

## 自动化任务

建议在 Cursor Automation 中创建两条任务：

- AI 日报：每天 `08:00 Asia/Macau`，使用 [prompts/cursor-ai-daily.md](prompts/cursor-ai-daily.md)。
- 股市日报：每天 `08:30 Asia/Macau`，使用 [prompts/cursor-stock-daily.md](prompts/cursor-stock-daily.md)。

## 来源策略

采用“公开优先”策略：

- 官方博客、RSS、公司 IR、SEC EDGAR、HKEXnews、主流媒体优先。
- X/Facebook 只作为补充来源，必须验证官方账号。
- 无法访问或无法验证的消息必须在报告中标注为缺口或待确认。
- 报告不提供买卖建议，只描述可能影响和后续观察点。
