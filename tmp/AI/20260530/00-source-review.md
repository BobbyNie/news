# AI 来源重检 — 20260530

## 数据窗口

- **报告日期（澳门时区）**：2026-05-30
- **生成时间**：2026-05-30 07:00（澳门时间，取自 automation `triggeredAt` 2026-05-29T23:00:37.470Z）
- **采集窗口**：2026-05-28 07:00 ~ 2026-05-30 07:00（澳门时间 UTC+8）
- **对应市场日历**：美股 5/28–5/29（周四、周五）有交易；港股 5/29（周五）收盘；5/30（周六）无港股/美股常规交易

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| Anthropic Series H 官方稿 | 官方 | 5/28 融资与估值、收入 run-rate、算力合作披露 | 已用于本日 P0；长期保留 `anthropic.com/news` |
| Micron / Samsung / SK hynix（Anthropic 股东名册） | 战略投资者 | 5/28 首次同现于头部 AI 公司 cap table，牵动 HBM 供应链叙事 | 在 `stock-sources.yaml` 与 AI 日报交叉引用 |
| Infineon × NVIDIA MGX 800VDC | 官方新闻稿 | 5/28–29 AI 数据中心供电架构 | 纳入算力基础设施专题 |
| OpenAI 5/28–29 Safety 系列帖 | 官方 | Frontier Governance、第三方评估、Rosalind | 监管/安全专题临时跟踪 |
| Dell FY26 Q1（AI 服务器） | 上市公司披露 | 5/29 业绩驱动全球 AI 硬件情绪 | 股市日报主源；AI 日报引用为算力需求信号 |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| 低可信度聚合（opentools.ai、bearbull.io 等） | 降权 | 仅转述 CNBC/官方，不作唯一事实源 |
| 未验证的 OpenAI「已递交 S-1」二手站 | 标注待 SEC | 保密递交不在 EDGAR 公开；以 CNBC/公司声明为准 |

## 今日访问缺口

- **Bloomberg / WSJ 全文**：Anthropic 融资细节部分需订阅
- **X/Facebook**：未系统抓取；重大事件以官网与 CNBC 交叉
- **arXiv**：窗口内无与 P0 事件直接绑定的同行评议新稿
- **中国 AI 公司官网**（智谱、月之暗面、DeepSeek 等）：窗口内无重大可验证官方发布

## 需要人工确认的来源

- **OpenAI 保密 IPO**：CNBC 称「未来数日/数周」可能递交；**EDGAR 仍无公开注册文件** → 标注「待 SEC/公司确认」
- **Anthropic Mythos 全面公开时间表**：官方称「未来数周」，无具体日期
- **Mythos 与 Opus 4.8 是否为同一产品线的不同能力档位**：以 Anthropic 官方产品/安全博客为准

## 重检结论

过去 48 小时**无需永久新增 AI 公司**至 `ai-sources.yaml`；建议在股市清单强化 **HBM 三巨头作为 Anthropic 战略股东** 的跟踪，并继续将 **OpenAI / Anthropic / SpaceX** IPO 叙事作为本周交叉主题。
