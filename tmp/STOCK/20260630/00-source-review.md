# 2026-06-30 股市日报来源重检

- 数据窗口：2026-06-28 12:02 ~ 2026-06-30 12:02（澳门时间 UTC+8）
- 日期依据：`python3 scripts/report_date.py` 输出 `REPORT_DATE=20260630`；澳门时间周二，不触发周报。

## 新增建议

- 暂不新增固定股票或固定人物来源。今日股票选择由可核验事件触发：美股 6 月 29 日收盘、Dow 成分变动、Comcast 重组、港股新上市、Bending Spoons / Ares SPAC / Sinda 等 IPO 线索。
- 可继续使用 AP / Investopedia / MarketWatch 作市场收盘交叉验证；IPO 仍优先 SEC、HKEX、NYSE、Nasdaq、Renaissance、IPOScoop。

## 失效或降权建议

- 社媒帖子只作为线索，不作为事实来源。
- HKEX 页面可访问，但其中“Newly Listed Securities”包含结构性产品、权证、债券和交易安排；不得全部当作经营公司 IPO。

## 今日访问缺口

- Micron IR 直接 `curl -I` 返回 403，但仍保留公司 IR URL；若写入细节，需标注抓取受限。
- Bloomberg、WSJ、FT 部分全文受限；使用 AP、Investopedia、S&P Global、HKEX、NYSE、Renaissance、IPOScoop 交叉验证。

## 需要人工确认的来源

- Bending Spoons、CopperTech、ITG、Lime 等 IPO 最终定价和交易日需继续核对 SEC/Nasdaq/NYSE 文件。
- 港股 2026-06-30 新上市项目需继续区分普通公司 IPO、H 股、债券、结构性产品与交易安排。
