# Scoring Rules

Use explainable ranking. The user should be able to see why each task made the brief.

## Factors

Priority:

- P0: highest.
- P1: high.
- P2: normal.
- P3: low.
- Missing priority: treat as P2 and mention the default if it affects selection.

Date:

- Tasks with `日期` today or overdue rise sharply.
- Tasks dated within 3 days rise moderately.
- No date does not imply unimportant; rely on priority, relations, title, and notes.

Origin:

- User-explicit tasks get a boost when this is clear from the title or `备注`.
- Tasks linked through `关联计划` get a boost when the learning plan is due today.
- Review follow-ups get a boost the day after creation when `备注` says `复盘跟进`.
- Topic-derived items stay below core tasks unless explicitly promoted or urgent.

Schedule fit:

- Schedule rows with `状态 = 进行中` matching today's cadence or `下次推进 <= today` get a boost.
- Schedule rows get a stronger boost when they clearly relate to today's tasks through `关联计划`, shared keywords, or support relationships in `备注`.
- Daily-cadence Schedule rows do not all become tasks automatically; without relevance to today's task context, include at most one public-course baseline item and at most one foundation baseline item.
- Public-course tasks should combine course content and assignment / exercise progress when feasible.
- Foundation baseline tasks must name a concrete topic and include a reason and minimal done criterion. Reject vague candidates such as "learn one math point" or "review a basic principle".
- Stale learning plans get review visibility, but not automatic selection over deadlines.

Deferral and blockers:

- `延期` tasks should appear in Risks / Waiting until the user reschedules them.
- `阻塞` tasks should appear only when there is a clear follow-up action.
- Deferral reasons and blockers live in `备注` in MVP.

Work mode:

- If the user gives a work-mode constraint such as "今天只能读文献" or "上午适合 coding", use the task title, relations, schedule context, and notes to choose compatible tasks.
- Do not require dedicated energy or context fields in MVP; infer work mode from title, relations, schedule context, and `备注`.

Balance:

- Avoid selecting only one type of task every day unless deadlines require it.
- Prefer a mix of core work, learning, and one maintenance item when feasible.

## Selection Procedure

1. Filter out `已完成`, `取消`, and irrelevant blocked tasks.
2. Rank hard deadlines first when `备注` makes them clear; otherwise rank by `日期`.
3. Add Schedule / Learning Plan candidates that support today's task context.
4. If no relevant learning item exists, add at most one due public-course baseline candidate and at most one due foundation baseline candidate. The foundation candidate must name a concrete topic before it can be selected.
5. Add high-priority user-intent and follow-up tasks.
6. Review stale or deferred tasks for inclusion or risk listing.
7. Pick 3-5 main tasks.
8. Put non-selected urgent or blocked tasks under Risks / Waiting.

## Overload Handling

When deadlines, blockers, or too many urgent tasks make the learning load questionable, do not silently remove learning. Ask the user to choose one of:

- keep the public-course and foundation baseline items;
- shrink to one small learning item;
- skip learning today and update `下次推进`.

## Explanation Format

For each selected task, include one short reason:

```text
Why today: dated tomorrow, P1, and it unblocks the Learning Plan.
```

If ranking is uncertain because fields are missing, say so and suggest the missing field to add.
