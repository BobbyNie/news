# 股市来源重检 — 20260528

## 数据窗口

- **报告日期（澳门时区）**：2026-05-28
- **生成时间（澳门）**：2026-05-28 07:02（取自 automation triggeredAt: 2026-05-27T23:02:33Z）
- **采集窗口**：2026-05-26 07:02 ~ 2026-05-28 07:02（澳门时间，UTC+8）
- **市场日历**：美股 5/27（周三）全日交易；港股 5/27 已收盘

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| CNBC Live Markets（5/26–5/27） | 主流媒体 | 道指新高、原油、Micron/SK Hynix、白宫辟谣 Hormuz | 纳入每日大盘首选 |
| Bloomberg（Qualcomm–ByteDance、SK Hynix 视频） | 主流媒体 | 5/26–5/27 AI ASIC 与 HBM 叙事 | 股市日报引用；标注订阅墙 |
| SCIO 国务院新闻办英文稿 | 官方 | 5/25 CSRC 跨境券商处罚 | 与 CNA 5/22 交叉 |
| Investing.com | 行情转述 | SK Hynix 万亿市值时间与韩元报价 | 须与 CNBC 交叉并标注时间 |
| beincrypto / stocksdownunder | 二级 | 5/27 芯片获利了结、Hormuz 辟谣 | 仅补充情绪，价格以 CNBC 为准 |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| Trading Economics CFD 报价 | 降权 | 恒指点位与港交所收盘略有偏差，以 CNBC/财联社为准 |
| coinfomania 等加密导向站 | 降权 | 券商整治文夹杂 crypto 叙事 |
| ECMsource / Meyka 单一来源收盘价 | 降权 | Micron 收盘价需以 CNBC/Yahoo 交叉 |

## 今日访问缺口

- **HKEXnews**：未逐条检索当日公告 PDF
- **SEC EDGAR**：未批量扫描 watchlist 8-K；SpaceX S-1 沿用 5/20 公开件
- **公司 IR**：Qualcomm、ByteDance **未**就 ASIC 协议发布官方新闻稿（Bloomberg 引「知情人士」）
- **实时报价**：文末指数/个股以 **2026-05-27 美股收盘或当日文中标注时间** 为准，盘后不保证延续

## 需要人工确认的来源

- **伊朗 Hormuz 复航**：伊朗官方媒体称一个月内恢复通行 → **白宫称「完全捏造」**（CNBC 5/27）→ 油价波动驱动需标注不确定性
- **Qualcomm–ByteDance**：Bloomberg 5/26 私人谈判报道，双方未回复记者问询
- **Micron 5/27 收盘涨幅**：CNBC 称较前日 mega-cap 行情收涨 **+3.6%**（非盘前 +8% 峰值）

## 重检结论

建议将 **内存/HBM 超级周期**（MU、000660.KS、005930.KS）与 **Qualcomm 数据中心 ASIC** 列为本周 `stock-sources.yaml` 专题观察；跨境券商整治对 **FUTU、TIGR** 及港股资金面影响延续跟踪。无新增永久 IR 域名需写入清单。
