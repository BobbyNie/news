# 2026-06-23 股市日报来源重检

- 报告日期：20260623 / 2026-06-23
- 数据窗口：2026-06-21 12:01 ~ 2026-06-23 12:01（澳门时间 UTC+8）

## 新增建议

- AP market wrap 可作为美股指数与行业表现交叉验证来源，适合在 Reuters/Bloomberg 受限时补充。
- HKEX Newly Listed Securities 继续作为港股近期 IPO 的 primary source。
- Nasdaq IPO Calendar / SEC EDGAR 继续用于美股 IPO primary source；若公司无 SEC registration statement，不写成确定上市。

## 失效或降权建议

- 未发现 stock-sources.yaml 既有来源需要删除。
- 仅有社媒传播的 SpaceX/SPCX、xAI、Tesla 交易线索全部降权，除非有 SEC、IR、交易所或公司公告。

## 今日访问缺口

- Reuters、Bloomberg、FT、WSJ 部分市场报道受登录或付费限制。
- 港股个股实时价格的官方页面不稳定，本次港股只写可核验的指数/新上市/公告级事实。
- 美股部分澳门午间距离完整美股收盘有时间差；价格与指数使用主流媒体市场 wrap 和公开报价，标注来源时间。

## 需要人工确认的来源

- 近期 IPO 的发行价、募资额、锁定期与首日表现应继续回查 SEC prospectus、Nasdaq IPO Calendar、NYSE IPO Center、HKEX prospectus / allotment results。
- 马斯克相关资产若出现 SpaceX/SPCX 二级市场或公开产品，必须等待 SEC/Nasdaq/公司文件。
