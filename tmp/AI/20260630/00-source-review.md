# 2026-06-30 AI 日报来源重检

- 数据窗口：2026-06-28 12:02 ~ 2026-06-30 12:02（澳门时间 UTC+8）
- 日期依据：`python3 scripts/report_date.py` 输出 `REPORT_DATE=20260630`；澳门时间周二，不触发周报。

## 新增建议

- 暂不新增固定来源。OpenAI、Anthropic、AWS、Snowflake、HSBC/LSEG 等仍可覆盖本窗口企业 AI、开发者工具和金融 AI 应用。
- 可继续观察 Releasebot/厂商 changelog 聚合页，但不能替代 Anthropic/OpenAI/AWS 官方来源。

## 失效或降权建议

- OpenAI 官方页在当前执行环境被 Cloudflare challenge 拦截；保留为一手来源入口，但在覆盖缺口中标注本次直接抓取受限。
- Micron、部分财经媒体页面存在访问防护或付费墙；涉及股票事实时优先使用公司 IR、AP、S&P Global 或交易所页面。

## 今日访问缺口

- OpenAI `openai.com/index/...` 直接 `curl -I` 返回 403 challenge，使用公开搜索摘要与既有官方 URL 作入口，避免引述无法复核的细节。
- Bloomberg、WSJ、FT 部分内容受限；未使用未验证社媒作为事实来源。

## 需要人工确认的来源

- 社媒账号只作为线索，不作为唯一事实来源。
- 金融业 AI 应用未发现窗口内新的银行一手公告；专栏保留并说明已检查来源与缺口。
