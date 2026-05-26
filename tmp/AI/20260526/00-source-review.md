# AI 来源重检 — 20260526

## 数据窗口

- **报告日期（澳门时区）**：2026-05-26
- **采集窗口**：2026-05-24 22:00 ~ 2026-05-26 22:00（澳门时间，UTC+8）
- **对应欧美日历**：约 2026-05-24 ~ 2026-05-26（含美国 Memorial Day 休市日）

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| SEC EDGAR — SpaceX (CIK 0001181412) | 官方披露 | 5/20 公开 S-1，与 xAI 整合、轨道 AI 算力叙事影响 AI 独角兽估值 | 纳入 `stock-sources.yaml` 交叉跟踪；AI 日报引用 IPO/融资语境时链至 S-1 |
| Google I/O 2026 专题页 | 官方活动 | 5/19–20 集中发布 Gemini 3.5、Spark、Gemini for Science | 临时跟踪至 6/10；长期可并入 Google DeepMind / blog.google |
| IEEE ISCAS 2026（华为 τ 定律） | 会议/官方稿 | 5/25 何庭波主题演讲，驱动半导体与国产 AI 算力叙事 | 与华为官网新闻稿交叉；勿仅用二手「韬定律」译名 |
| Vatican — Magnifica Humanitas | 官方文件 | 5/25 教宗首部通谕聚焦 AI 监管，Anthropic 联合创始人出席 | 监管/伦理专题补充，非日常公司源 |
| Binance Pre-IPO 合约（OPENAIUSDT） | 市场基础设施 | 5/26 上线 OpenAI 预 IPO 永续 | 仅作融资情绪补充，**不得**作为 IPO 事实唯一来源 |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| 无 | — | 清单内官方博客/RSS 仍可访问；本次未发现需移除项 |
| 低可信度聚合站（scramnews、mindwiredai 等） | 降权 | 仅转述 WSJ/CNBC，不单独引用为事实源 |

## 今日访问缺口

- **Bloomberg** 部分文章需订阅，DeepSeek 融资细节以 Yahoo/Reuters 转述为准
- **X (@OpenAI 等)**：本次未逐条抓取；重大事件以 openai.com/news 为准
- **Facebook 官方**：Meta 裁员以 Bloomberg 报道为主，Facebook 视频为二次传播
- **arXiv 全文**：AlphaProof Nexus、OpenAI 数学证明仅引用摘要与官方/媒体说明
- **中国公司官网**（智谱、月之暗面等）：5/26 窗口内无重大官方新闻稿可验证

## 需要人工确认的来源

- OpenAI **保密递交 IPO**：CNBC/WSJ 5/20 报道「最早周五递交」，截至 5/26 **未在 SEC EDGAR 检索到 OpenAI 公开注册文件** → 标注「待 SEC/公司确认」
- Meta **泄露音频**（Model Capability Initiative）：主流媒体转述 More Perfect Union，**待 Meta 官方新闻稿或 SEC 8-K 确认**措辞
- OpenAI 数学模型是否为「未发布 reasoning 模型」：官方称 internal model，具体产品名未公开

## 重检结论

过去 48 小时无必须永久写入 `ai-sources.yaml` 的新 AI 公司；建议将 **SpaceX S-1（含 xAI 分部）** 在股市清单强化，AI 日报继续以现有官方公司列表为主，并补充 **Google I/O 2026** 与 **教宗 AI 通谕** 作为本周专题跟踪。
