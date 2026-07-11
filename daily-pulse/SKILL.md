---
name: daily-pulse
description: "Use when the user wants a Notion-first daily operating workflow: morning planning, daily task orchestration, learning schedule review, topic intelligence, evening reflection, task status updates, or follow-up creation from a daily review."
---

# Daily Pulse

## Overview

Daily Pulse is a Notion-first daily operating workflow. Use it to turn Tasks, Schedule / Learning Plan items, and lightweight Topics configuration into a morning brief, then run a deep evening review that writes task and learning-plan state back to Notion.

The skill defines single-run behavior. Scheduling must come from Codex automations, reminders, monitors, or an external scheduler.

## Required Config

Load runtime configuration from:

```text
~/.codex/state/daily_pulse_config.json
```

Required shape:

```json
{
  "notion": {
    "tasks_data_source_id": "<uuid>",
    "daily_pulse_data_source_id": "<uuid>",
    "schedule_data_source_id": "<uuid>"
  },
  "topics_config_path": "/absolute/path/to/topics.yaml",
  "timezone": "Asia/Shanghai",
  "notification": {
    "mode": "chat",
    "target": null
  }
}
```

If the config or a required field is missing, stop and report the missing field. Do not guess Notion database IDs.

## Choose The Flow

- Morning brief: use [morning-brief.md](references/morning-brief.md).
- Evening review: use [evening-review.md](references/evening-review.md).
- Schema setup, field mapping, or Notion database questions: use [notion-schema.md](references/notion-schema.md).
- Runtime config setup or troubleshooting: use [configuration.md](references/configuration.md).
- Adding a course, knowledge point, technical route, routine, or learning plan: use [schedule-intake.md](references/schedule-intake.md).
- Ranking or "why did you choose these tasks" questions: use [scoring-rules.md](references/scoring-rules.md).
- Topic paper recommendations or hotspot tracking: use [topic-briefing.md](references/topic-briefing.md).

If the user asks for a full Daily Pulse without specifying morning or evening, infer from local time:

- Before 14:00: run the morning brief.
- At or after 18:00: run the evening review.
- Otherwise ask whether they want morning planning or evening review.

## Notion Access

Prefer available Notion MCP/app tools for reads and writes. Use data source IDs from config. If tool names are unclear, search for Notion tools whose names include search, fetch, database, page, create, or update; do not invent tool names.

Default to search/fetch reads unless config explicitly enables SQL/query mode. Some Notion workspaces require Enterprise + Notion AI for `query_data_sources`, so a failed SQL query should fall back to data-source search plus page fetch rather than stopping the whole flow.

When writing to Notion:

- Create or update one Daily Pulse record per date.
- Relate selected tasks to the Daily Pulse record when the schema supports relations.
- Use the user's existing property names if a mapping exists; otherwise use the default schema in [notion-schema.md](references/notion-schema.md).
- Report any write failure and avoid making contradictory partial updates.

## Write Guardrails

Allowed writes:

- Create or update today's Daily Pulse record.
- Mark selected morning tasks as `今日`.
- Create concrete tasks from Schedule / Learning Plan `下一步行动`.
- Create follow-up tasks from the evening review.
- Update task status and notes.
- Update Schedule / Learning Plan progress, next action, and next due.

Do not:

- Delete Notion records.
- Mark a task `已完成` without explicit user confirmation or an unambiguous evening review answer.
- Silently create topic-derived tasks in MVP. Present them as suggested tasks unless the user asks for automatic creation.
- Send third-party notifications in MVP. Output to Codex chat and write to Notion.

## Output Style

This skill is intentionally heavier than a notification bot. Prefer a structured daily report with clear rationale over a terse reminder. Keep prose concise, but include enough reasoning for task choices, schedule pressure, and risks to be auditable later from the Daily Pulse record.
