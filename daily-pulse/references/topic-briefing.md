# Topic Paper Recommendations

Topics are paper-first. Use the local YAML file from `topics_config_path`; do not require a Notion Topics database. Treat each configured topic as a paper recommendation lane, not a general news lane.

## Config Shape

```yaml
topics:
  - name: "Agent memory"
    priority: medium
    keywords:
      - "agent memory"
      - "long-term memory agents"
    sources:
      - huggingface_daily_papers
      - arxiv
      - openreview
      - project_page
    min_papers: 3
    max_papers: 5
    action_threshold: "create suggested task only when clearly relevant"
```

## Workflow

1. Load the YAML config.
2. Read recent Notion context as personalization signals only from the configured personalization root page and its child pages. Do not use Daily / Daily Pulse / Tasks / Schedule as personalization sources, because that creates self-reinforcing topic loops.
3. Read the previous evening's paper candidate pool when available. The evening review should have collected the top 10 most-liked Hugging Face Daily Papers as the next day's first-pass candidate pool.
4. For each active topic, select papers from the candidate pool when they are directly related or cross-domain useful.
5. If a topic has fewer than `min_papers`, supplement from current arXiv, OpenReview, project pages, or the user's Notion paper context.
6. For each active topic, recommend at least 3 and at most 5 papers.
7. Prefer primary sources: Hugging Face Daily Papers, arXiv, OpenReview, project pages, official paper pages, or publisher pages. GitHub may be included as a secondary code link only when useful, but it should not affect ranking.
   - If a paper is selected from the previous evening's Hugging Face Daily Papers candidate pool, its `来源` line must show both the Hugging Face Daily Papers link and the primary paper source link, for example: `来源：[Hugging Face Daily Papers](...)；主源：[arXiv](...)`.
   - If a paper is supplemented from arXiv/OpenReview/project pages rather than the Hugging Face candidate pool, label it explicitly, for example: `来源：[arXiv](...)；补充来源：非昨晚 HF top10，按 <topic> 主线补齐`.
8. Group related papers into a short narrative, but keep each recommendation individually attributable.
9. Add candidate actions to the morning brief as suggestions, not automatic tasks.

## Ranking Signals

Use these ranking signals for now:

1. Hugging Face Daily Papers rank / likes.
2. Freshness from arXiv, OpenReview, or paper/project page date.
3. Match with configured topic keywords.
4. Match with today's tasks and active learning plans.
5. Cross-domain transfer value for the user's current robotics / embodied AI / agent / research workflow work.
6. Personalization from the configured Notion context root.

Do not use academic impact or engineering usability as ranking signals for now:

- Ignore citation count, influential citations, citation velocity, h-index, venue prestige, and Semantic Scholar influence scores.
- Ignore GitHub stars, forks, issues, commit activity, release status, Papers with Code SOTA tables, and benchmark leaderboard rank.
- Code/project links may still be shown as source context, but they should not increase recommendation priority.

## Evening Candidate Pool

During evening review, if tools are available, collect the next day's first-pass paper pool:

1. Open Hugging Face Daily Papers for the current local date.
2. Record the top 10 papers by likes/upvotes.
3. Preserve title, paper URL, source URL, vote/like count if visible, and a one-line abstract-level note.
4. Write the candidate pool into the Daily Pulse page body under `## 明日论文候选池`.
5. Do not create tasks from this pool during evening review unless the user explicitly asks.

If Hugging Face is unavailable, state that the candidate pool could not be collected and use arXiv/OpenReview search during the next morning run.

## Morning Selection

During morning brief:

1. Start from the previous evening's Hugging Face top-10 candidate pool.
2. Keep only papers that match configured topic keywords, today's tasks, learning plans, or useful cross-domain transfer.
3. Supplement missing slots from arXiv/OpenReview/project pages until each active topic has 3-5 papers.
4. Label why each paper is selected:
   - `主线相关`: directly supports today's task or current Notion research thread.
   - `跨领域可迁移`: not directly in-topic but method/benchmark/tooling can transfer.
   - `背景补强`: useful foundation, not an urgent read.
5. Rank each paper as `精读`, `粗读`, or `收藏`.

## Output Template

```text
今日论文推荐

总判断：<2-4 sentences on today's paper pattern and what it means for the user's work>

## <configured topic name>

今日状态：<重点阅读 / 轻量阅读 / 背景补强, with reason>

### 1. <paper title>

来源：<arXiv / OpenReview / project page / publisher / Hugging Face Daily Papers link>

推荐级别：<精读 / 粗读 / 收藏>

选择原因：<主线相关 / 跨领域可迁移 / 背景补强, and why>

建议读法：<which sections, figures, method, experiments, or code to inspect>

对我有什么用：<what the user should read, compare, reproduce, or ignore>

### 2. <paper title>

...

### 3. <paper title>

...

## <next configured topic name>

...

今天最值得优先看的 5 个
1. <item>：<reason>
2. <item>：<reason>
3. <item>：<reason>
4. <item>：<reason>
5. <item>：<reason>
```

## Guardrails

- Do not let paper recommendations dominate today's core task list.
- Do not silently create Notion tasks from topic updates in MVP.
- If browsing or external tools are unavailable, say which topic checks could not be completed.
- Prefer primary sources for technical topics: paper pages, arXiv, OpenReview, publisher pages, or project pages.
- For recommendations that could change quickly, verify current information before including it.
- Do not write filler such as "monitor AI agents" without concrete paper evidence and relevance.
- Do not include unverified paper names, metrics, or code-release status. If a user provides an example format with unverified facts, copy the structure but verify facts before writing them into the daily brief.
- Each paper must have `来源`, `推荐级别`, `选择原因`, `建议读法`, and `对我有什么用`.
- Each item must include clickable source links. Prefer Hugging Face Daily Papers, arXiv, OpenReview, project pages, or publisher pages. If none are available, include the best information-source link and label it clearly.
- Source links should appear directly under the item title, before `发生了什么`.
- The brief must cover every active topic in `topics.yaml`; do not let one high-volume topic crowd out the rest.
- Each active topic must contain at least three and at most five papers.
- If a topic has no strong recent paper, include three useful background papers or recent adjacent papers and label the topic `背景补强`.
- Recommendations must be personalized from the configured Notion context root when available. Use child pages such as PaperReading, Idea, experiments, robot notes, project pages, and meeting notes to decide `对我有什么用` and the final top-3 ranking.
- If the configured context root is unavailable or search/fetch is partial, say so briefly and avoid over-personalizing.
- Never cite Daily Pulse's own generated pages as evidence for personalization.
- Do not use old benchmarks, surveys, or background resources as if they were today's topic updates. If an older resource is useful context, label it as `背景资源` and keep it outside the main three entries unless the topic explicitly lacks recent material.
- For fast-moving topics such as robotics and embodied AI, prioritize recent papers and paper/project pages over classic benchmarks.
- End with a ranked top-5 paper reading list.
