# Notion Schema

Use these Chinese schemas as defaults. If the user's Notion workspace already has similar databases, map existing properties instead of forcing exact names.

## Daily Pulse Tasks

Purpose: executable actions.

| Property | Type | Values / Notes |
|---|---|---|
| 任务 | Title | Required action sentence. |
| 状态 | Select | 收件箱, 已计划, 今日, 进行中, 已完成, 阻塞, 延期, 取消. |
| 优先级 | Select | P0, P1, P2, P3. |
| 日期 | Date | Planned date, review date, or deadline. Put hard-deadline context in `备注`. |
| 关联日报 | Relation | Daily Pulse record. |
| 关联计划 | Relation | Schedule / Learning Plan item. |
| 备注 | Text | Origin, hard deadline, blocker, progress, deferral reason, or review notes. |

Status meanings:

- `收件箱`: captured but not planned.
- `已计划`: valid task, not today.
- `今日`: selected in the current morning brief.
- `进行中`: started.
- `已完成`: completed.
- `阻塞`: cannot progress without an external condition.
- `延期`: intentionally pushed forward.
- `取消`: no longer relevant.

## Daily Pulse

Purpose: one operational record per day.

| Property | Type | Values / Notes |
|---|---|---|
| 名称 | Title | `Daily Pulse YYYY-MM-DD`. |
| 日期 | Date | Calendar date. |
| 早报 | Text | Short summary only. Put the formatted morning report in the page body. |
| 晚间复盘 | Text | Short summary only. Put the formatted evening review in the page body. |

Morning creates or updates the record. Selected tasks link back through their `关联日报` property. Long reports should be written to the Daily Pulse page body, not stuffed into text properties.

## Daily Pulse Schedule

Purpose: courses, knowledge points, routines, and technical routes.

| Property | Type | Values / Notes |
|---|---|---|
| 名称 | Title | Course, knowledge point, routine, or technical route name. |
| 类型 | Select | 公开课, 知识点, 习惯, 项目路线. |
| 状态 | Select | 进行中, 暂停, 已完成, 归档. |
| 节奏 | Select | 每天, 工作日, 每周, 自定义. |
| 下一步行动 | Text | Next concrete learning action. |
| 进度 | Text | Example: `Lecture 3/16`. |
| 下次推进 | Date | Next suggested appearance. |
| 备注 | Text | Cadence details, preferred weekdays, resources, context, and constraints. |

Schedule rows are planning objects, not daily tasks. The morning flow should create or select concrete Tasks from `下一步行动`.

When a user says they want to learn a knowledge point, public course, paper route, or technical route, do not require them to provide every field. Use [schedule-intake.md](schedule-intake.md) to ask only the missing questions needed to create a useful Schedule row.

## Field Mapping

If existing Notion property names differ, create an explicit mapping in config or in the run notes:

```json
{
  "field_map": {
    "tasks": {
      "任务": "Name",
      "日期": "When"
    }
  }
}
```

Prefer mapping over renaming user databases.
