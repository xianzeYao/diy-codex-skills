# Evening Review

Use this flow for evening reflection, "review today", "复盘今天", or scheduled evening runs.

## Workflow

1. Load config and resolve today's date.
2. Find today's Daily Pulse record.
3. Fetch tasks linked to today's Daily Pulse through `关联日报`, plus related Schedule / Learning Plan rows.
4. Ask the review questions in chat.
5. Parse answers into task outcomes, blockers, energy, decisions, follow-ups, and tomorrow adjustments.
6. Update Tasks:
   - completed items to `已完成`;
   - blocked items to `阻塞` and record the blocker in `备注`;
   - deferred items to `延期` and record the deferral reason in `备注`;
   - continuing items to `已计划` or leave `今日` if explicitly planned for tomorrow;
   - new follow-ups with the reason recorded in `备注`.
7. Update Schedule / Learning Plan:
   - update `进度` from the user's report;
   - update `下一步行动` when the next step changes;
   - update `下次推进` from cadence.
8. Write a short summary to Daily Pulse `晚间复盘`, then write the formatted evening review to the Daily Pulse page body. Include outcomes, blockers, energy, tomorrow adjustments, and unresolved items in the page body.
9. If tools are available, collect Hugging Face Daily Papers top 10 by likes/upvotes as the next morning's candidate pool. Write them under `## 明日论文候选池` in the Daily Pulse page body. Do not create tasks from these papers unless the user explicitly asks.
10. Return a concise evening summary in chat.

## Review Prompt

```text
Evening Review

First, today's main tasks:
1. <task> - done, partial, blocked, or deferred?
2. <task> - done, partial, blocked, or deferred?
3. <task> - done, partial, blocked, or deferred?

Then:
- What was the biggest reason today went well or poorly?
- How was your energy and time allocation?
- What should change tomorrow?
- Any follow-up tasks I should create?
```

Ask follow-up questions only when needed to write correct state. For example, if the user says "partial", ask what progress should be recorded and what the next action is.

## Page Body Template

```text
# Evening Review - YYYY-MM-DD

## 今日结论

**总判断：** <1-3 sentences>

## 任务结果

### <task>

**状态：** 已完成 / 部分完成 / 阻塞 / 延期

**完成了什么：**
- ...

**没完成 / 卡住的原因：**
- ...

**下一步：**
- ...

## 学习计划更新

- <Schedule item>: <progress / next action / next due>

## 精力与时间

- <energy and time allocation>

## 明日调整

- <specific changes for tomorrow>

## 未闭环事项

- <follow-up tasks or questions>

## 明日论文候选池

来源：Hugging Face Daily Papers top 10 by likes/upvotes, collected during evening review.

1. <paper title> - <source link> - <likes/upvotes if visible> - <one-line note>
2. ...
```

## Chat Summary Template

```text
晚间复盘已写入 <Daily Pulse page link>.

状态更新:
- <task>: <status>
- <task>: <status>

明日调整:
- <one or two changes>
```

## Write Guardrails

- Do not mark `已完成` unless the user clearly confirms completion.
- If a task is partially completed, preserve it as `已计划` or `延期` and update `备注` with progress.
- Record deferral reason in `备注`; do not require a separate deferral counter in MVP.
- If the user mentions a new action item, create it as a task and note `复盘跟进` in `备注` unless they say not to.
- Do not put the full review into the `晚间复盘` property. Keep that property as a one-line or short-paragraph summary and put the formatted review in the page body.
- The Hugging Face Daily Papers top-10 pool is a candidate pool, not the final recommendation list. The next morning brief must filter it by configured topics and the user's current work, then supplement from arXiv/OpenReview/etc. as needed.
- If multiple writes fail, report which succeeded and which failed.
