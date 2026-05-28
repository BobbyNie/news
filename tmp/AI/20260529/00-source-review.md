# AI 来源重检 — 20260529

## 数据窗口

- **报告日期（澳门时区）**：2026-05-29（由 `triggeredAt` 2026-05-28T23:00:04.876Z 换算）
- **生成时间**：2026-05-29 07:00（澳门时间）
- **采集窗口**：2026-05-27 07:00 ~ 2026-05-29 07:00（澳门时间 UTC+8）
- **对应主要市场日历**：美股 5/27–5/28（美东）交易；港股 5/28 收盘

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| Anthropic Series H 新闻稿 | 官方 | 5/28 披露 650 亿美元融资、9650 亿美元估值及与 SpaceX Colossus 算力协议 | 已纳入今日 P0；长期保留官方链接 |
| OpenAI Frontier Governance Framework | 官方 | 5/28 发布，对齐加州 SB 53 / EU GPAI 实践 | 纳入监管专题跟踪 |
| France 24 / AFP 转述 Altman、Huang 就业表态 | 主流媒体 | 5/28 行业领袖软化「就业末日」叙事 | 作社会/劳工专题补充，交叉 The Australian 原报道 |
| TechCrunch Google AI Overviews 拼写争议 | 主流媒体 | 5/27–28 搜索质量舆论 | 产品信任风险专题，需 Google 官方声明（已引 TechCrunch 邮件回应） |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| CryptoBriefing 等加密媒体 | 降权为次要 | SpaceX–Anthropic Colossus 租约以 Anthropic 官方 Series H 稿为准 |
| ChatGPT/Finbold 股价预测 | 禁止入报 | 非可验证事实 |
| Meyka、Officechai 二次解读 | 降权 | 模型/融资以 anthropic.com 为准 |

## 今日访问缺口

- **Bloomberg / WSJ 全文**：Anthropic 估值对比 OpenAI 部分依赖 CNBC、Decoder 转述
- **X (@elonmusk 等)**：Colossus 租约细节未逐条抓取；以 Anthropic 官方融资稿中 SpaceX 合约为准
- **Meta / 中国大厂官网**：窗口内无重大可验证新闻稿
- **arXiv**：无窗口内重磅论文单独收录

## 需要人工确认的来源

- **SpaceX Colossus 租约「独家」范围**：官方稿写「access to GPU capacity in Colossus 1 and Colossus 2」；媒体称六个月独家，需 SpaceX IR 或 SEC 文件进一步确认
- **Anthropic 965B 估值 vs OpenAI 私募估值**：媒体报道口径不一，以 Anthropic 官方 post-money 为准
- **Google AI Overviews 拼写错误**：已复现报道，修复时间表未官方公布

## 重检结论

过去 48 小时**无需**永久新增公司至 `ai-sources.yaml`；建议将 **Anthropic Series H + Opus 4.8** 与 **OpenAI 治理框架** 列为本周 P0 跟踪，**SpaceX 算力合作** 与股市清单交叉引用。
