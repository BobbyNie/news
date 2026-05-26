# Cursor Automation Prompt: 股市日报

你在 `/Users/bobbynie/gitStore/news` 工作。请生成今日股市新闻中文 HTML 日报。

严格按以下步骤执行：

0. **必须先运行** `eval "$(python3 scripts/report_date.py)"`，用输出的 `REPORT_DATE` / `REPORT_ISO` / `REPORT_MONTH` / `REPORT_WINDOW` 作为唯一日期依据。**禁止使用 UTC 或系统默认时区日期**（UTC 23:00 时澳门已是次日）。
1. 读取 `sources/stock-sources.yaml` 和 `sources/source-review-rules.md`。
2. 先重检清单：搜索过去 24-48 小时是否有新的美股/港股重点公司、AI 独角兽、IPO、SEC/HKEX 披露、官方 IR 来源或主流市场媒体需要加入跟踪。把结果写入 `tmp/STOCK/YYYYMMDD/00-source-review.md`。
3. 按清单检索 SEC EDGAR、HKEXnews、公司 IR、新闻稿、主流财经媒体和可信市场新闻。把原始发现写入 `tmp/STOCK/YYYYMMDD/01-raw-findings.md`。
4. 去重、按市场影响排序，把候选新闻写入 `tmp/STOCK/YYYYMMDD/02-ranked-items.md`。
5. 生成中文草稿到 `tmp/STOCK/YYYYMMDD/03-draft-cn.md`。
6. 用中文生成 HTML 报告到 `YYYY-MM/STOCK/YYYYMMDD.html`。报告必须包含：今日最重要 5-10 条、美股重点、港股重点、AI 独角兽/IPO、财报与指引、监管与风险、明日继续跟踪、来源覆盖与缺口。
7. 每条重要判断必须附来源链接，价格、涨跌、市值等实时数据必须注明时间和来源。不要给买卖建议。
8. 完成后运行 `python3 scripts/build_pages_index.py` 更新根目录 `index.html`。
9. **必须** `git add`、`git commit`、`git push origin main`。commit message: `daily stock news report ${REPORT_ISO}`。
10. 确认 push 成功；GitHub Actions `Publish News Pages` 会在 push 到 `main` 后自动部署 Pages。

## 输出要求

- 使用澳门时区日期。
- 英文来源需翻译成中文并保留原文链接。
- 价格、涨跌、市值、盘前盘后数据必须注明时间、市场和来源。
- 对未上市独角兽只描述融资、估值、IPO、监管和重大商业事件，不做估值建议。
- 不提供买卖建议，只写“可能影响”和“需要继续跟踪”。

## HTML 结构

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YYYY-MM-DD 股市日报</title>
</head>
<body>
  <h1>YYYY-MM-DD 股市日报</h1>
  <section id="window">更新时间与数据窗口</section>
  <section id="top">今日最重要的 5-10 条</section>
  <section id="us">美股重点</section>
  <section id="hk">港股重点</section>
  <section id="unicorns">AI 独角兽 / IPO</section>
  <section id="earnings">财报与指引</section>
  <section id="risks">监管与风险</section>
  <section id="next">明日继续跟踪</section>
  <section id="coverage">来源覆盖与缺口</section>
</body>
</html>
```
