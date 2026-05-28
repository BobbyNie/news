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

1. 读取 `sources/ai-sources.yaml` 和 `sources/source-review-rules.md`。
2. 先重检清单：搜索过去 24-48 小时是否有新的重点 AI 公司、官方来源、X/Facebook 官方账号、主流媒体专题或论坛来源需要加入跟踪。把结果写入 `tmp/AI/YYYYMMDD/00-source-review.md`。
3. 按清单检索官方博客、RSS、新闻稿、主流媒体、X/Facebook、论坛、研究社区。公开官方来源优先，X/Facebook 仅作为补充，必须验证官方账号。把原始发现写入 `tmp/AI/YYYYMMDD/01-raw-findings.md`。
4. 去重、按重要性排序，把候选新闻写入 `tmp/AI/YYYYMMDD/02-ranked-items.md`。
5. 生成中文草稿到 `tmp/AI/YYYYMMDD/03-draft-cn.md`。
6. 用中文生成 HTML 报告到 `YYYY-MM/AI/YYYYMMDD.html`。报告必须包含：今日最重要 5-10 条、主题详情、公司跟踪表、风险与不确定性、明日继续跟踪、来源覆盖与缺口。
7. 每条重要判断必须附来源链接。不要编造无法验证的信息。
8. 完成后检查 `git diff` 和 `git status`，提交当日变更。commit message: `daily AI news report YYYY-MM-DD`。

## 输出要求

- **报告日期与文件名必须使用澳门时区**，且以 `automation_trigger_info.triggeredAt` 换算结果为准（见上文「日期与时间」）。
- 英文来源需翻译成中文并保留原文链接。
- 重要判断必须有可点击来源链接。
- X/Facebook 内容只作为补充信号，除非能确认官方账号。
- 无法访问的来源要在“来源覆盖与缺口”列出。
- 不写投资建议。

## HTML 结构

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YYYY-MM-DD AI 日报</title>
</head>
<body>
  <h1>YYYY-MM-DD AI 日报</h1>
  <section id="window">更新时间与数据窗口</section>
  <section id="top">今日最重要的 5-10 条</section>
  <section id="details">分主题详情</section>
  <section id="companies">公司跟踪表</section>
  <section id="risks">风险与不确定性</section>
  <section id="next">明日继续跟踪</section>
  <section id="coverage">来源覆盖与缺口</section>
</body>
</html>
```
