# Topic Briefing

Topics are lightweight in MVP. Use a local YAML file from `topics_config_path`; do not require a Notion Topics database.

## Config Shape

```yaml
topics:
  - name: "Agent memory"
    priority: medium
    keywords:
      - "agent memory"
      - "long-term memory agents"
    sources:
      - arxiv
      - github
      - web
    max_items: 3
    action_threshold: "create suggested task only when clearly relevant"
```

## Workflow

1. Load the YAML config.
2. Read recent Notion context as personalization signals only from the configured personalization root page and its child pages. Do not use Daily / Daily Pulse / Tasks / Schedule as personalization sources, because that creates self-reinforcing topic loops.
3. For each active topic, gather current signals only from available tools and allowed sources.
4. Prefer primary sources: arXiv, project pages, official docs, GitHub repos, company announcements, or credible reporting for industry events.
5. Group related signals into a short narrative instead of listing disconnected links.
6. Add candidate actions to the morning brief as suggestions, not automatic tasks.

## Output Template

```text
今日 AI / 具身智能 / 机器人简报

总判断：<2-4 sentences on the main pattern, not a list of links>

## <configured topic name>

今日状态：<重点更新 / 轻量监控 / 今天无高价值更新, with reason>

### 1. <item title>

来源：<arXiv / GitHub / project page / official announcement / source link>

发生了什么：<specific update, numbers if verified, source type>

为什么重要：<technical or workflow implication>

对我有什么用：<what the user should read, try, monitor, or ignore>

### 2. <item title>

来源：<...>

发生了什么：<...>

为什么重要：<...>

对我有什么用：<...>

### 3. <item title>

来源：<...>

发生了什么：<...>

为什么重要：<...>

对我有什么用：<...>

## <next configured topic name>

...

今天最值得优先看的 3 个
1. <item>：<reason>
2. <item>：<reason>
3. <item>：<reason>
```

## Guardrails

- Do not let topic updates dominate the morning brief.
- Do not silently create Notion tasks from topic updates in MVP.
- If browsing or external tools are unavailable, say which topic checks could not be completed.
- Prefer primary sources for technical topics: papers, official docs, repository releases, or project pages.
- For recommendations that could change quickly, verify current information before including it.
- Do not write filler such as "monitor AI agents" without concrete evidence and relevance.
- Do not include unverified paper names, metrics, or code-release status. If a user provides an example format with unverified facts, copy the structure but verify facts before writing them into the daily brief.
- Each item must have three subparts: `发生了什么`, `为什么重要`, and `对我有什么用`.
- Each item must include clickable source links. Prefer arXiv, GitHub, project pages, official docs, or company announcements. If none are available, include the best information-source link and label it clearly.
- Source links should appear directly under the item title, before `发生了什么`.
- The brief must cover every active topic in `topics.yaml`; do not let one high-volume topic crowd out the rest.
- Each active topic must contain at least three concrete entries. Entries can be papers, repos, product/docs updates, project pages, benchmark resources, or a clearly sourced technical argument.
- If a topic has no strong recent update, include three useful monitoring entries or foundational resources and label the topic `轻量监控`.
- Recommendations must be personalized from the configured Notion context root when available. Use child pages such as PaperReading, Idea, experiments, robot notes, project pages, and meeting notes to decide `对我有什么用` and the final top-3 ranking.
- If the configured context root is unavailable or search/fetch is partial, say so briefly and avoid over-personalizing.
- Never cite Daily Pulse's own generated pages as evidence for personalization.
- Do not use old benchmarks, surveys, or background resources as if they were today's topic updates. If an older resource is useful context, label it as `背景资源` and keep it outside the main three entries unless the topic explicitly lacks recent material.
- For fast-moving topics such as robotics and embodied AI, prioritize recent papers, project pages, code releases, or company updates over classic benchmarks.
- End with a ranked top-3 reading/action list.
