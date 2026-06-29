# 2026-06-29 STOCK 来源重检

- 数据窗口：2026-06-27 12:01 ~ 2026-06-29 12:01（澳门时间 UTC+8）
- 日期依据：`python3 scripts/report_date.py` 输出 `REPORT_DATE=20260629`。

## 新增建议

- HKEX Newly Listed Securities 在 2026-06-29 显示 TESTCO25、GRACE CLW2506、BEIJING PHARMA 等新上市项目；港股 IPO/新上市栏目继续优先检查该页面：https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities?sc_lang=en
- The Guardian 2026-06-29 AI 硬件报道可作为市场主题背景，具体股票仍需公司披露或金融数据验证：https://www.theguardian.com/technology/2026/jun/29/small-ai-cheaper-chips-nvidia-competitors

## 失效或降权建议

- 未发现 `stock-sources.yaml` 中交易所/IPO 一手来源失效。
- 对 IPO 质量判断不使用固定 watchlist；仅基于 HKEX、NYSE、Renaissance、IPOScoop 等当前页面和披露触发。

## 今日访问缺口

- 周末后美股尚未开出 2026-06-29 正常交易日，实时美股价格只能延续 2026-06-26 收盘/快照或使用当前可得页面。
- 部分 Reuters、Bloomberg、WSJ 正文受限；如使用 syndication 或摘要，已在报告中列为缺口。

## 需要人工确认的来源

- HKEX 6 月 29 日新上市中部分为结构性产品或非普通股，正文不应强行解读成公司 IPO。
- Bending Spoons、Sinda 等 IPO 候选需要继续读取 SEC/交易所文件，当前仅作观察和继续跟踪。
