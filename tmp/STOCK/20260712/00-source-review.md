# 2026-07-12 STOCK 来源重检

- 数据窗口：2026-07-10 12:01 ~ 2026-07-12 12:01（澳门时间 UTC+8）
- 日期 provenance：本次环境未暴露 `automation_trigger_info.triggeredAt`；按任务上下文的澳门周日使用代理 trigger `2026-07-12T04:01:12Z` 运行 `scripts/report_date.py`。

## 新增建议

- AP 7 月 10 日美国指数收盘与 SK Hynix Wall Street debut：用于正式收盘与 IPO 事实。
- HKEX Newly Listed Securities：用于确认 7 月 10 日 Nexchip、Hesai-W、Befar 等港股上市事件。
- MarketWatch / Barron's 周日油价与期货：用于周末地缘风险，但不写成正式收盘。

## 失效或降权建议

- 不新增固定股票 watchlist；本次只覆盖窗口内由交易所、公司披露、主流媒体和正式市场数据触发的标的。
- 对社媒、YouTube 市场评论和未注明时间的价格截图降权。

## 今日访问缺口

- WSJ、FT、Bloomberg 部分页面 paywall；可用片段仅作为交叉验证。
- 港股 7 月 12 日为周日，无新正式收盘；港股部分以 7 月 10 日上市清单和可访问报价页为基线。

## 需要人工确认

- Nexchip、Hesai-W、Befar 等 7 月 10 日新股的最终收盘、换手和配发细节建议用 HKEX/公司公告继续复核。
- 周日美股期货和油价为盘前/周末信号，不可当成正式股市收盘。
