# AI 原始发现 - 2026-06-18

## 1. OpenAI: A near-autonomous AI chemist improves a reaction

- 发布时间：2026-06-17
- 来源名称：OpenAI
- 原文链接：https://openai.com/index/ai-chemist-improves-reaction/
- 可信度：official
- 中文摘要：OpenAI 称 GPT-5.4 与 Molecule.one 的 Maria AI / high-throughput lab 连接后，为 Chan-Lam coupling 找到 TEMPO / 4-hydroxy-TEMPO 等添加剂思路。Maria Lab 共运行 10,080 个反应，优化条件下 88% boronic acids 和 83% sulfonamides 的测得产率改善；人工 bench-scale 验证 14 组中 11 组提升。官方同时强调人类化学家仍负责 steering、proposal selection、plan correction 和 bench validation。

## 2. OpenAI: Introducing LifeSciBench

- 发布时间：2026-06-17
- 来源名称：OpenAI
- 原文链接：https://openai.com/index/introducing-life-sci-bench/
- 可信度：official
- 中文摘要：LifeSciBench 是面向真实生命科学研究任务的 benchmark，包含 750 个专家撰写任务、1,062 个任务附件、173 位 scientist contributors、19,020 条 rubric criteria 和 453 位 expert reviewers。重点不是事实问答，而是评估模型在证据处理、实验设计、科学推理、验证运营、转化判断和科学沟通中的研究实用性。

## 3. OpenAI: Deployment Simulation

- 发布时间：2026-06-16
- 来源名称：OpenAI
- 原文链接：https://openai.com/index/deployment-simulation/
- 可信度：official
- 中文摘要：OpenAI 发布 Deployment Simulation 方法，用真实历史对话语境模拟新模型部署，以在上线前估计 undesired model behavior，并称已用于 GPT-5-series Thinking deployments 和复杂 agent settings / tool use 轨迹。该线索与 6 月 17 日生命科学研究更新共同显示 OpenAI 正在强化模型能力评估和发布前风险控制。

## 4. Anthropic opens Seoul office and Korean partnerships

- 发布时间：2026-06-17
- 来源名称：Anthropic
- 原文链接：https://www.anthropic.com/news/seoul-office-partnerships-korean-ai-ecosystem
- 可信度：official
- 中文摘要：Anthropic 宣布开设 Seoul office，并与韩国 Ministry of Science and ICT 签署 MOU，合作 AI safety、cybersecurity、Korean-language model safety evaluation 和 AI-enabled cyber threats 信息交流。采用案例包括 NAVER 全工程组织使用 Claude Code、Nexon 用 Claude Code 支持 live-service game engineering、LG CNS / Samsung SDS / Hanwha / Channel Corp / Good Neighbors Korea 等。

## 5. AWS Context for data and AI agents

- 发布时间：2026-06-17
- 来源名称：AWS Machine Learning Blog
- 原文链接：https://aws.amazon.com/blogs/machine-learning/context-intelligence-for-your-data-and-ai-agents-at-scale/
- 可信度：official
- 中文摘要：AWS 在 Summit New York City 宣布 context intelligence 系列更新，其中 AWS Context 将企业数据关系映射为 knowledge graph，并为 AI agents 提供 governed relationships、business rules 和 curated context。Amazon Quick 的个人知识图谱能力扩展到组织层 context layer。

## 6. Amazon Quick autonomous agents

- 发布时间：2026-06-17
- 来源名称：AWS Machine Learning Blog
- 原文链接：https://aws.amazon.com/blogs/machine-learning/get-back-hours-every-day-with-autonomous-agents-in-amazon-quick/
- 可信度：official
- 中文摘要：Amazon Quick 增加 autonomous agents、activity feed 和跨数据源提问能力。用户可用自然语言创建持续运行的 agents，并通过 guardrails 控制自治程度。属于企业 productivity agents 从助手走向后台执行的产品化信号。

## 7. SageMaker AI Async Inference inline payloads

- 发布时间：2026-06-17
- 来源名称：AWS Machine Learning Blog
- 原文链接：https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads/
- 可信度：official
- 中文摘要：Amazon SageMaker AI Async Inference 支持直接在 InvokeEndpointAsync 请求中传入 payload，最大 128,000 bytes，减少每次调用前上传 S3 的网络往返和客户端复杂度，适合 bursty 或 batch-style inference workloads。

## 8. NVIDIA / Coherent Texas optical backbone

- 发布时间：2026-06-17
- 来源名称：NVIDIA Blog
- 原文链接：https://blogs.nvidia.com/blog/coherent-texas-ai-optical/
- 可信度：official
- 中文摘要：NVIDIA 报道 Coherent Sherman, Texas 扩建项目，包含 5,000 万美元 CHIPS Act grant 和此前 Texas CHIPS / local support。文章强调 indium phosphide、gallium arsenide、lasers、transceivers 和 optical modules 对 AI data center networking 的重要性，并提到 Vera Rubin Ultra NVL576 这类大规模 GPU 域需要 silicon photonics。

## 9. TCS / Anthropic regulated industries baseline

- 发布时间：2026-06-12
- 来源名称：Anthropic
- 原文链接：https://www.anthropic.com/news/tcs-anthropic-partnership
- 可信度：official
- 中文摘要：TCS 与 Anthropic 合作，将 Claude 提供给 50,000 名员工，并为金融服务、医疗、公共部门等 regulated industries 构建 Claude-powered products。金融用例包括 insurer claims processing、bank lending advisory、Claude Code 支持银行金融服务产品团队的软件工程与 IT operations。

## 10. DXC / Anthropic banks and regulated systems baseline

- 发布时间：2026-06-11
- 来源名称：Anthropic
- 原文链接：https://www.anthropic.com/news/dxc-anthropic-alliance
- 可信度：official
- 中文摘要：DXC 与 Anthropic 建立 multi-year global alliance，DXC 将训练 Claude-certified forward-deployed engineers，把 Claude 集成到其为大型 banks、airlines、insurers、manufacturers、government agencies 运行的 mission-critical systems。DXC 表示 Claude 是 OASIS agentic workflows 的默认基础模型。
