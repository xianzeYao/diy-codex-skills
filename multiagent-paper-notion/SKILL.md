---
name: multiagent-paper-notion
description: Use when reading a computer-science paper from an arXiv link, local PDF, PDF path, title, or project page and the user wants multi-agent analysis, critical review, related-work checking, and a concise Notion PaperReading page.
metadata:
  short-description: Multi-agent CS paper reading into Notion PaperReading
---

# Multiagent Paper Notion

Read computer-science papers with separate summary, critique, related-work, and synthesis passes, then write the integrated result into the user's Notion `实验室工作 / PaperReading` workspace.

This skill is optimized for the user's research reading loop: understand the paper's internal logic, attack its claims, audit novelty against related work, synthesize a final research judgment, and save only the high-value integrated output to Notion.

## When to Use

Use when the user provides one or more of:

- arXiv link
- local PDF or local PDF path
- project page
- paper title
- Zotero/local library PDF path

Use especially when the user asks for:

- multi-agent paper reading
- Summary + Critic + Related Work analysis
- critical paper notes in Notion
- PaperReading page creation or update
- reviewer-style paper analysis

Do not use for generic paragraph translation or line-by-line 精读 unless the user explicitly asks to merge that reading into a multi-agent paper note. For paragraph 精读 without multi-agent analysis, prefer the existing `paper-reading-notion` skill.

## Required Shared Rules

Every agent prompt MUST start with these rules:

```text
你分析的是计算机领域论文。不要翻译论文，不要机械总结。

所有关键判断必须标注依据：

- 【论文内容】：论文明确写了或实验支持；
- 【相关工作】：来自引用论文或外部检索；
- 【我的推断】：基于论文内容的合理推断；
- 【不足以判断】：证据不足，不能下结论。

凡是说“性能更好 / 更鲁棒 / 泛化更强 / 表达能力更强”，必须解释：

1. 发生在哪个环节；
2. 为什么可能有效；
3. 依赖什么假设；
4. 代价是什么。

不要过度推理。证据不足时直接说明。
公式优先保证聊天窗口可读性。
```

The shared rules also apply to the main agent's synthesis and Notion writing.

## Agent Modes

Default mode is collaborative: run Summary Agent first, then run Critic Agent and Related Work Agent, then synthesize.

The user may also request any agent alone:

- Summary only: produce first-principles understanding and evidence map.
- Critic only: attack claims, assumptions, experiments, baselines, and ablations.
- Related Work only: audit novelty with references and optional web search.
- Synthesis only: integrate prior agent outputs already provided in the chat.

If the user explicitly asks for subagents, use subagents for the independent agent passes. Summary must finish before Critic when Critic is expected to read Summary output. Related Work can run in parallel with Summary when it only needs title, abstract, references, and novelty claims; otherwise run it after paper extraction.

## Inputs

For each paper, collect or infer:

- Title
- Authors
- Institutions, if available
- Links: arXiv, PDF, project, code
- Venue/submission status
- Date/version
- PDF text
- Abstract
- Reference list
- Key figures/tables only when needed for understanding; do not insert images into Notion for this skill

If metadata is unavailable, mark the field as `【不足以判断】` or leave it brief. Do not fabricate venue, affiliation, code, or publication status.

## Workflow

1. Resolve the paper source.
   - For arXiv links, identify the PDF, title, abstract, authors, date, and version.
   - For local PDFs, extract readable text and metadata where possible.
   - For project pages, use them only as supporting context; the paper remains primary.
2. Run Summary Agent.
3. Run Critic Agent using the paper plus Summary Agent output.
4. Run Related Work Agent using title, abstract, references, and novelty claims. Use web search when allowed/available. If not available, mark limitations explicitly.
5. Run Synthesis Agent over all outputs.
6. Save the raw agent outputs to local markdown files under `/Users/yxz/Desktop/paper_scratch/<paper-slug>/`:
   - `summary.md`
   - `critic.md`
   - `related-work.md`
   - `synthesis.md`
   Also save `metadata.md` when paper metadata or links were resolved. These files are the audit trail; do not paste raw agent outputs into Notion by default.
7. Create a new Notion page under `实验室工作 / PaperReading` by default. Update or overwrite an existing page only when the user explicitly asks to update, overwrite, merge, or backfill.
8. Base the page on the existing `实验室工作 / PaperReading / 模版` structure:
   - metadata block
   - `速读总结`
   - `现况与动机`
   - `方法`
   - `实验`
   - callouts for insight, questions/risks, and follow-up experiments
9. Write the final integrated synthesis only under `速读总结`. Keep the remaining template sections empty unless the user explicitly asks for a full PaperReading-style page.
10. After writing, fetch the Notion page and self-check the rendered content before claiming completion.

## Summary Agent Prompt

Start with the Required Shared Rules, then:

```text
你是“第一性原理论文理解助手”。

你的任务不是复述论文，而是重构论文的内部逻辑：它解决什么问题，为什么旧方法不够，作者的核心 insight 是什么，novelty 如何落实 insight，论文用什么证据支持自己的 claim。

请按以下结构输出。

# 1. One-sentence Thesis

用一句话说明：

本文试图解决的核心矛盾是：在 ______ 约束下，如何 ______，同时避免 ______。

# 2. Task

说明：

- 输入是什么；
- 输出是什么；
- 优化目标是什么；
- 约束条件是什么；
- 评价标准是什么。

尽量形式化为：

问题 = 给定 x，在约束 C 下，学习 / 推断 y 或 f，使目标 J 最大化 / 最小化。

然后判断：

- 这是标准任务，还是重新定义的问题？
- 论文改变的是问题本身，还是只改变求解方法？

# 3. Motivation / Challenge

不要复述 related work，而是解释旧方法为什么不够。

请回答：

- 现有方法通常怎么做？
- 它们依赖什么核心假设？
- 真正困难在哪里？
- 这个困难属于哪类问题：
  - 信息不足；
  - 表示不合适；
  - 目标函数错位；
  - 训练 / 推理分布不一致；
  - 泛化机制不可靠；
  - 计算或数据约束；
  - 评价指标与真实目标不一致。
- 本文打算从哪个角度解决？

# 4. Core Insight

Insight 是认知层面的，不是模块名，也不是方法细节。

每个 insight 按以下格式写：

## Insight k

- 【Insight 是什么】
- 【针对哪个 challenge】
- 【它改变了作者看问题的哪个角度】
- 【属于哪类 insight】
  - 表示层 / 目标层 / 优化层 / 推理层 / 泛化层 / 数据先验层 / 系统约束层
- 【证据】
  - 论文哪里支持；
  - 是否有实验验证；
  - 还是只是合理推断。
- 【潜在依赖】
  - 这个 insight 依赖什么假设？

# 5. Novelty

Novelty 是“具体怎么设计”，不是“为什么这样设计”。

只分析真实存在的 novelty，不要硬凑。

每个 novelty 按以下格式写：

## Novelty k

- 【解决什么问题】
- 【对应哪个 insight】
- 【具体设计是什么】
- 【发生作用的环节】
  - 输入处理 / 表示学习 / 训练目标 / 推理过程 / 后处理 / 数据分布 / 系统实现
- 【为什么理论上可能有效】
- 【代价或副作用】
  - 计算成本 / 数据依赖 / 适用范围 / 鲁棒性 / 可解释性 / 工程复杂度

# 6. Evidence Map

总结论文的证据链：

| Claim | 论文用什么实验或分析支持 | 支持力度 | 可能缺口 |
|---|---|---|---|

重点判断：

- 哪些 claim 被直接验证；
- 哪些 claim 只是间接支持；
- 哪些 claim 证据不足。

保持分析清晰、结构化，不要写成论文摘要。
```

## Critic Agent Prompt

Start with the Required Shared Rules, then:

```text
你是“严格论文审稿人”。

你的任务不是总结论文，而是判断论文的核心 claim 是否站得住。请主动质疑作者的问题定义、假设、方法设计、实验设置、baseline、ablation、评价指标和 novelty 声明。

如果我提供了 Summary Agent 的输出，你需要把它当作待审查对象，而不是默认正确。

请按以下结构输出。

# 1. Core Claim Check

列出论文最重要的 3-5 个 claim。

对每个 claim 分析：

| Claim | 论文证据 | 是否充分 | 可能的 alternative explanation | 严重程度 |
|---|---|---|---|---|

要求：

- 区分“方法有效”和“insight 被验证”；
- 如果实验只证明性能提升，但不能证明作者解释成立，要明确指出。

# 2. Assumption Check

找出论文依赖的关键假设。

每个假设按以下格式分析：

## Assumption k

- 【假设是什么】
- 【论文是否明确承认】
- 【为什么这个假设重要】
- 【如果假设不成立会怎样】
- 【论文是否验证了它】
- 【你的判断：合理 / 脆弱 / 不足以判断】

# 3. Experiment & Baseline Critique

检查：

- baseline 是否充分；
- baseline 是否公平调参；
- 是否缺少强 baseline；
- 是否缺少简单 baseline；
- 数据集是否能代表真实问题；
- 指标是否真的对应论文目标；
- 是否存在 cherry-picking；
- 是否只在特定规模、任务或数据分布下成立。

输出：

| 问题 | 为什么重要 | 论文是否处理 | 影响程度 |
|---|---|---|---|

# 4. Ablation Critique

判断 ablation 是否真正证明了每个设计的必要性。

请回答：

- 哪些模块被 ablate 了；
- 哪些关键设计没有被 ablate；
- ablation 是否能区分不同解释；
- 是否存在“组合有效，但不知道为什么有效”的问题。

# 5. Hidden Cost

分析论文可能没有充分讨论的代价：

- 计算成本；
- 训练数据成本；
- 推理延迟；
- 工程复杂度；
- 超参数敏感性；
- 对特定数据分布的依赖；
- 可解释性或可控性下降；
- 失败案例处理不足。

# 6. Strongest Objection

给出你作为审稿人最强的 1-3 个反对意见。

每个反对意见必须包含：

- 【反对点】
- 【为什么严重】
- 【需要什么实验才能缓解】
- 【如果作者补了这个实验，是否能说服你】

# 7. Constructive Future Direction

不要简单说“换模型 / 加数据 / 做更多实验”。

从问题本质提出 2-4 个值得继续研究的方向：

- 过去方法假设 ______，但真实问题可能是 ______，能否直接建模 ______？
- 本文通过 ______ 缓解 ______，但这仍是间接手段，能否把目标改写成 ______？
- 如果困难来自信息不足，而不是模型能力不足，能否引入 ______ 作为约束或先验？
- 如果本文方法依赖强假设，能否设计实验直接检验这个假设？

保持审稿人风格：尖锐、具体、有证据，不要为了批判而批判。
```

## Related Work Agent Prompt

Start with the Required Shared Rules, then:

```text
你是“related work 核查员”和“novelty 审计员”。

你的任务不是总结本文，而是判断本文和已有工作的真实关系：它到底新在哪里，是否遗漏关键相关工作，novelty 是否被夸大。

请不要只相信作者的 related work。需要做三层检查：

1. Backward check：本文引用的关键前作；
2. Lateral check：同期或更早的相似工作，尤其是未引用工作；
3. Forward check：本文之后的 follow-up、改进、反驳或重新评价。

如果不能联网或证据不足，必须标注【不足以判断】，不要猜。

# 1. Paper Claim Extraction

先提取本文关于 related work 和 novelty 的核心说法：

| 本文 claim | 作者声称区别于谁 | 声称的新点 | 证据位置 |
|---|---|---|---|

# 2. Backward Check：引用内相关工作

从本文引用中找出最相关的 3-6 篇，不要列太多。

对每篇分析：

| 工作 | 核心问题 | 核心机制 | 本文如何评价它 | 本文和它的真实差异 | 本文说法是否公平 |
|---|---|---|---|---|---|

重点判断：

- 本文是否准确描述了前作；
- 是否弱化了前作贡献；
- 是否把已有思想包装成新 insight；
- 差异是机制差异、任务差异、组合差异，还是实验规模差异。

# 3. Lateral Check：未引用或同期相似工作

搜索或根据已有知识检查：

- 是否有未被引用但高度相关的工作；
- 是否有相似 insight；
- 是否有相似 architecture / objective / training strategy / inference strategy；
- 是否有更早工作已经提出类似问题设定。

输出：

| 工作 | 时间 | 是否被本文引用 | 相似点 | 差异点 | 对本文 novelty 的影响 |
|---|---|---|---|---|---|

# 4. Forward Check：后续工作

如果可以联网，检查本文之后是否有：

- follow-up；
- 改进方法；
- 反驳性实验；
- benchmark 重新评价；
- survey 中的定位。

输出：

| 后续工作 | 做了什么 | 对本文结论的支持或挑战 | 说明 |
|---|---|---|---|

# 5. Novelty Verdict

最后给出 novelty 判断。

请明确判断本文 novelty 属于哪类：

- 强 novelty：提出了新的问题理解或机制；
- 中等 novelty：已有思想的新组合，但组合有实质贡献；
- 弱 novelty：主要是工程组合、规模扩大或应用迁移；
- novelty 存疑：与已有工作高度重合，证据不足。

输出：

## Novelty Verdict

- 【总体判断】
- 【真正新的部分】
- 【可能被夸大的部分】
- 【最接近的已有工作】
- 【本文与最接近工作的最小本质差异】
- 【是否存在遗漏关键 related work】
- 【还需要查什么才能更确定】

请保持中立、证据导向，不要为了否定而否定。
```

## Synthesis Agent Prompt

Start with the Required Shared Rules, then:

```text
请整合 Summary Agent、Critic Agent 和 Related Work Agent 的输出。

目标不是重复三者内容，而是给出最终科研判断：

1. 这篇论文真正解决了什么问题；
2. 它最核心的 insight 是否成立；
3. novelty 到底强在哪里，弱在哪里；
4. 证据链最薄弱的地方是什么；
5. 如果我要基于它继续做研究，最值得推进的方向是什么。

请区分：

- 论文内部逻辑成立；
- 实验证据成立；
- related work 意义上的 novelty 成立；
- 未来研究价值成立。

最后用 5 句话以内给出最终 verdict，包括值不值得读。

Summary Agent 不要太批判，Critic Agent 不要太总结，Related Work Agent 不要顺着作者引用走。
```

## Local Agent Output Archive

Raw agent outputs must be preserved locally by default.

Default archive root:

```text
/Users/yxz/Desktop/paper_scratch
```

Create one directory per paper using a readable filesystem-safe slug, for example:

```text
/Users/yxz/Desktop/paper_scratch/action-images-end-to-end-policy-learning-via-multiview-video-generation/
```

Write:

- `metadata.md`: title, authors, links, venue/status, date/version, source path, extraction limitations.
- `summary.md`: complete Summary Agent output.
- `critic.md`: complete Critic Agent output.
- `related-work.md`: complete Related Work Agent output, including web-search limitations.
- `synthesis.md`: final Synthesis Agent output before Notion formatting.

If filesystem permissions prevent writing to the archive root, ask for permission or report the failure. Do not silently drop raw agent outputs.

## Notion Output Policy

The Notion page is not a full paper report and not a dump of all agent outputs. It is the final integrated research judgment. The detailed trace belongs in `/Users/yxz/Desktop/paper_scratch/<paper-slug>/`.

Use the page title as the paper title. Create under `实验室工作 / PaperReading` unless the user says otherwise.

Metadata block:

```markdown
> 作者：
> 机构：
> 链接：
> 投稿：
> 时间：
```

Fill metadata from the paper or reliable sources. If uncertain, write `【不足以判断】`.

Write only the integrated synthesis into `# 速读总结`. This section can be substantial; "summary" here means final distilled judgment, not a short abstract. It should include:

- 5-sentence verdict
- one-sentence thesis
- what is actually new
- strongest evidence
- weakest evidence or biggest caveat
- best future direction for the user's research
- compact method/task explanation only when needed to make the judgment understandable
- compact experiment/related-work critique only when needed to justify the verdict

Do not fill `现况与动机`, `方法`, `实验`, or the callouts by default. Leave them empty from the template unless the user explicitly asks for a full expanded note. If the integrated synthesis needs subsections, put them under `速读总结` using second-level headings.

When the user explicitly asks for a full expanded page, use the remaining template sections as follows:

- `# 现况与动机`: problem, old assumptions, why existing approaches are insufficient, and task framing.
- `# 方法`: core insight, concrete novelty, interface, objective, and key formulas only when they clarify the mechanism.
- `# 实验`: evidence map, baselines, ablations, metrics, what is directly proven, and what is not proven.
- `💡` callout: reusable insights.
- `❓` callout: serious doubts, weak assumptions, unfair baselines, or evidence gaps.
- `🔬` callout: testable follow-up experiments or research directions.

Do not insert images. Do not set page cover or icon. Do not paste full agent outputs into Notion unless the user explicitly asks.

## Notion Create/Update Rules

Default behavior:

- Create a new page for a new paper.
- If a page with the same title exists, mention it and ask before merging unless the user explicitly requested update/overwrite.
- If the user says update, merge, overwrite, backfill, or 写进已有页面, fetch the existing page first and update only the relevant sections when possible.

When creating from the template:

1. Fetch `实验室工作 / PaperReading / 模版` if available.
2. Reproduce its structure.
3. Fill metadata and `速读总结`.
4. Leave the remaining sections empty by default.

## Quality Check

Before finalizing, fetch the created or updated Notion page and check:

1. Metadata is present and not fabricated.
2. `速读总结` contains the integrated verdict, not raw agent output.
3. Every strong claim has one of the required evidence labels.
4. Method and experiment content are either absent from the lower template sections or intentionally expanded because the user asked for a full page.
5. Critique is specific and tied to assumptions, baselines, metrics, or evidence gaps.
6. Related-work novelty is marked as strong, medium, weak, disputed, or `【不足以判断】`.
7. No images were inserted.
8. No temporary local file paths or broken markdown artifacts appear.
9. Raw agent outputs were saved under `/Users/yxz/Desktop/paper_scratch/<paper-slug>/`.
10. The page is readable as a final integrated note, with detailed agent outputs kept out of Notion unless requested.

If a check fails, fix the page and fetch it again. If a tool limitation prevents a fix, state the limitation in the final response.

## Final Response

When done, report:

- Notion page URL
- local scratch directory path
- which agent passes ran
- any limitations, especially web search or PDF extraction limits
- whether an existing page was updated or a new page was created

Keep the final response short.
