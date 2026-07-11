# Morning Brief

Use this flow for morning planning, "today's tasks", "what should I work on", "generate today's Daily Pulse", or scheduled morning runs.

## Workflow

1. Load `~/.codex/state/daily_pulse_config.json`.
2. Resolve local date using config timezone.
3. Find or create today's Daily Pulse record.
4. Read candidate Tasks:
   - `日期` today or overdue;
   - high priority and open;
   - tasks currently marked `延期`;
   - user-created or unscheduled tasks found by title / `备注`;
   - blocked tasks that need follow-up.
5. Read active Schedule / Learning Plan rows:
   - `状态 = 进行中`;
   - cadence or weekday details in `节奏` / `备注` match today;
   - `下次推进 <= today`;
   - stale or repeatedly skipped according to `进度` / `备注`.
6. Match Schedule rows against today's task context before selection:
   - direct relation through `关联计划`;
   - overlapping keywords in task title, task `备注`, Schedule `名称`, `下一步行动`, or `备注`;
   - support relationship, such as math foundations supporting an AI / robotics task.
7. Convert selected Schedule rows into concrete task candidates using `下一步行动`.
   - For public courses, the task should include both course content and the related assignment / exercise when feasible.
   - For foundation routes, first choose a specific topic, then generate the task. Do not output placeholders like "learn one concept", "review one principle", or "do one exercise".
   - Foundation-route task titles must name the topic directly, and the task body or notes must include why this topic was selected and a minimal done criterion.
8. Read Topics config and build a paper-only topic recommendation section. Start from the previous evening's Hugging Face Daily Papers top-10 candidate pool when available, then supplement from arXiv/OpenReview/etc. until each active topic has 3-5 papers.
9. Score and rank candidates with `scoring-rules.md`.
10. Select 3-5 main tasks.
11. Mark selected tasks as `今日` unless already `进行中`.
12. Relate selected tasks to today's Daily Pulse when supported.
13. Write a short summary to Daily Pulse `早报`, then write the formatted report to the Daily Pulse page body.
14. Return the daily report in chat.

When rewriting or refining an existing morning report, preserve a `今日论文推荐` section. If no topic creates an action, still include each checked topic with 3-5 paper recommendations so the user can see that topic tracking ran.
Do not put the full morning report into a database text property. Use the page body for readable formatting and keep `早报` as a one-line or short-paragraph summary.

Use `query_data_sources` only when available. If it fails because the Notion workspace lacks Enterprise + Notion AI, use data-source search to find likely rows, then fetch each row page to read properties. In search/fetch mode, make the brief conservative and mention that ranking was based on partial search results.

## Page Body Template

```text
# Daily Pulse - YYYY-MM-DD

## 今日执行

### 1. <task>

**目标：** <one sentence>

**操作清单**
- <step>
- <step>

**完成标准**
- <observable completion>
- <observable completion>

**为什么今天做：** <deadline, schedule fit, priority, deferral, or user intent>

### 2. ...

## 今日论文推荐

<use topic-briefing.md structure>

## 暂缓
- <deferred item and reason>

## 晚间复盘入口
- <questions to answer tonight>

## 写入记录
- <records created or updated>
```

## Chat Summary Template

```text
今天看 Daily 页面里的「今日任务」视图。

今日任务:
1. <task> - <done criterion>
2. <task> - <done criterion>

完整早报已写入 <Daily Pulse page link>.
```

## Selection Rules

- Default to 3-5 main tasks.
- Prefer learning-plan tasks that support today's existing tasks.
- If several daily learning plans are due but none clearly relates to today's tasks, include at most one public-course baseline item and at most one foundation baseline item.
- A public-course baseline item should pair course content with assignment / exercise work, for example "Lecture 1 notes + assignment setup".
- A foundation baseline item must be specific. Pick a named topic from the route, such as `KL divergence`, `matrix multiplication shapes`, `Bayes rule`, `gradient descent`, `SE(3) transform composition`, or `Jacobian`, then explain why it is today's baseline.
- If deadlines or blockers would make learning unrealistic, ask the user whether to keep, shrink, or skip today's learning items instead of silently dropping them.
- Do not let topic intelligence replace core tasks unless the topic creates a clear same-day action.
- Paper recommendations are not tasks by default. Do not create PaperReading pages or Daily Pulse Tasks from recommendations unless the user explicitly asks.
- If too many tasks are urgent, show the top 5 and put the rest under Risks / Waiting.
- If there are fewer than 3 legitimate tasks, show fewer rather than inventing work.

## Write Behavior

Allowed:

- Create today's Daily Pulse record.
- Update `早报` summary and Daily Pulse page body.
- Mark selected tasks `今日`.
- Create a task from a due Schedule `下一步行动` if no matching open task exists.

Avoid:

- Marking tasks `已完成`.
- Creating topic-derived tasks without user confirmation.
- Changing Schedule progress during the morning flow unless the user explicitly reports progress.
