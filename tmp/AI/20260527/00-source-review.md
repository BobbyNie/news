# AI 来源重检 — 20260527

## 数据窗口

- **报告日期（澳门时区）**：2026-05-27
- **采集窗口**：2026-05-25 22:00 ~ 2026-05-27 22:00（澳门时间，UTC+8）
- **对应欧美日历**：约 2026-05-25 ~ 2026-05-27（美股 5/27 周三正常交易）

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| Polymarket 私营公司预测市场（OpenAI/Anthropic IPO） | 市场情绪 | 5/19 起多家媒体引用其 IPO 时序/估值概率 | 仅作融资情绪补充，**不得**作为 IPO 事实唯一来源；可写入 AI 日报「风险」节 |
| Investing.com / MEXC 等行情转述 | 二级媒体 | SK Hynix、Micron 万亿市值与 AI 算力叙事交叉 | 股市日报引用；AI 日报仅在「算力基础设施」节链至 CNBC/Bloomberg 一手 |
| SCIO / 新华社英文稿（跨境券商整治） | 官方 | 5/25 发布 CSRC 对 Futu/Tiger/Longbridge 处罚说明 | 已在 `stock-sources.yaml` 监管语境覆盖；AI 日报不重复除非涉及 AI 独角兽融资通道 |
| Qualcomm–ByteDance ASIC（Bloomberg 5/26） | 主流媒体 | 字节豆包/火山引擎算力供应链信号 | 股市日报「AI 独角兽」交叉；暂不永久写入 `ai-sources.yaml` |
| TipRanks / FinanceFeeds（Anthropic 收入超 OpenAI） | 财经媒体 | 5/27 密集转述 ARR 对比 | 引用时标注「媒体估算、待公司 IR/招股书确认」 |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| Instagram / Ozor 等社媒短视频 | 降权 | OpenAI S-1「已递交」表述无 SEC 可公开验证件，易与 CNBC 5/20「筹备递交」混淆 |
| YouTube 播客（Google $40B Anthropic 等） | 降权 | 未找到 Anthropic/Google 官方新闻稿交叉，本次不写入 Top 10 |
| Medium 个人专栏（IPO Wars） | 降权 | 无一手链接，仅作背景 |

## 今日访问缺口

- **SEC EDGAR**：SpaceX S-1（5/20）可公开检索；**未见 OpenAI 主体公开 Form S-1**（保密 DRS 若存在亦不对公众披露）
- **Bloomberg 全文**：SK Hynix、Qualcomm–ByteDance、DeepSeek 等需订阅
- **X**：Karpathy 入职帖已有多家媒体转述，本次未逐条抓取原帖
- **Anthropic 新闻详情页**：5/26 韩国代表理事任命稿 URL 未稳定抓取，以 Anthropic Newsroom 列表日期为准
- **中国公司官网**（智谱、月之暗面等）：窗口内无重大可验证官方发布

## 需要人工确认的来源

- **OpenAI 保密递交日期**：CNBC 5/20 称「最早周五（5/23）前后」筹备 confidential draft；FinanceFeeds/EnterpriseDNA 等称 **5/22 已递交** → 公开 EDGAR **无法验证**，标注「待 SEC 公开修订稿或公司确认」
- **Anthropic ARR $45B vs OpenAI $33B**（TipRanks 5/27）：非两家公司官方同期披露，可能与 gross vs net 收入口径有关（Vucense 等曾提示 SEC 口径风险）
- **Google 向 Anthropic 投资 $40B**：仅见播客/二手转述，**本次不采信为事实**

## 重检结论

过去 48 小时无必须永久写入 `ai-sources.yaml` 的新 AI 实验室；建议继续在 `stock-sources.yaml` 跟踪 **内存/HBM 周期**（Micron、SK Hynix、三星）与 **跨境券商整治** 对港股 AI 标的资金面的影响。AI 清单维持现有官方公司列表，本周专题延续 **IPO 竞赛**、**华为 τ 定律**、**Codex 自改进 Agent**。
