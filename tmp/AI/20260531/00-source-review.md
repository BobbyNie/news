# AI 来源重检 — 20260531

## 数据窗口

- **报告日期（澳门时区）**：2026-05-31
- **生成时间**：2026-05-31 07:02（澳门时间，取自 automation `triggeredAt` 2026-05-30T23:02:27.507Z）
- **采集窗口**：2026-05-29 07:02 ~ 2026-05-31 07:02（澳门时间 UTC+8）

## 新增建议

| 来源 | 类型 | 理由 | 建议动作 |
|------|------|------|----------|
| Micron / Samsung / SK hynix（经 Anthropic 官方稿） | 战略基础设施伙伴 | Series H 公告将三大存储厂商列为「strategic infrastructure partners」，反映 HBM 供应链与模型扩缩容绑定 | 在 `ai-sources.yaml` 的 `compute_infrastructure` 下增加「存储/HBM 战略伙伴」备注；股市日报交叉跟踪 |
| Ramp 企业 AI 采用数据 | 第三方用量统计 | 多家媒体引用 Ramp 称 Anthropic 4 月企业采用率超 OpenAI | 仅作补充指标，需后续核对 Ramp 原始发布 |
| OpenAI Education for Countries（edunewsletter.openai.com） | 官方子域 | 5/29 亚美尼亚国家级教育合作 | 纳入官方博客/RSS 跟踪列表 |
| Computex 2026 / GTC Taipei（NVIDIA） | 官方活动 | 5/29 预告「A new era of PC」，黄仁勋 6/1 主题演讲 | 临时跟踪至 6/10；与 Vera Rubin、光子学产能叙事联动 |

## 失效或降权建议

| 来源 | 建议 | 证据 |
|------|------|------|
| 无永久移除项 | — | 清单内 Anthropic、OpenAI、Google 官方页可访问 |
| Invezz、Make Tech Easier、Office Chai 等 | 降权 | 转述 Anthropic 官方与 CNBC，不单独作为估值唯一来源 |
| Cryptonomist 等加密媒体 | 降权 | 融资报道以 anthropic.com/news 为准 |

## 今日访问缺口

- **Bloomberg / FT 全文**：DeepSeek 融资、NVDA 部分细节以 TechCrunch、Let's Data Science 转述 FT 为准
- **X/Facebook**：未系统抓取；Anthropic/OpenAI 重大发布以官网为准
- **anthropic.com/news** 页面本次抓取超时，以具体文章 URL（series-h、claude-opus-4-8）为准
- **中国公司官网**（智谱、月之暗面、通义等）：窗口内无重大可验证官方稿
- **arXiv 2605.22763（AlphaProof Nexus）**：仅引用论文摘要与 DeepMind/GitHub 说明，未全文核验

## 需要人工确认的来源

- Anthropic **$965B 估值**与 **$47B ARR**：以 [官方 Series H](https://www.anthropic.com/news/series-h) 为准；二级市场/衍生品不得当作股权定价
- OpenAI **IPO 时间表**：窗口内无新 SEC 公开注册；继续标注「待 SEC 确认」
- Ramp **企业采用率超越 OpenAI**：媒体转述，待 Ramp 或 Anthropic 二次确认原始数据
- DeepSeek **$45B 融资**：FT 5/6 与 5/29 转述，**交易未官宣闭合**，标注「谈判中」

## 重检结论

过去 48 小时**无**必须永久新增至 `ai-sources.yaml` 的 AI 公司；建议强化 **存储/HBM 战略伙伴**与 **Computex/GTC Taipei** 临时跟踪。本窗口最大事件为 **Anthropic Series H + Claude Opus 4.8**，属既有清单公司官方来源，无需新增主体。
