# Configuration

Daily Pulse uses local runtime config for private IDs and paths. Do not hard-code Notion IDs in `SKILL.md`.

## Runtime Config

Path:

```text
~/.codex/state/daily_pulse_config.json
```

Template:

```json
{
  "notion": {
    "tasks_data_source_id": "<tasks-data-source-id>",
    "daily_pulse_data_source_id": "<daily-pulse-data-source-id>",
    "schedule_data_source_id": "<schedule-learning-plan-data-source-id>"
  },
  "topics_config_path": "/Users/yxz/Documents/Codex/diy-codex-skills/daily-pulse/topics.yaml",
  "personalization_root_page_url": "https://app.notion.com/p/1a82735ce8f98095b0f1c7c5ea92b4dd",
  "timezone": "Asia/Shanghai",
  "notion_read_mode": "search_fetch",
  "notification": {
    "mode": "chat",
    "target": null
  }
}
```

## Finding Data Source IDs

Use Notion's data source ID, not the parent database ID. If a Notion database URL is available, fetch it with the Notion tool and copy the `collection://...` data source URL or UUID from the result.

Store only the UUID in config:

```json
"tasks_data_source_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

If the tool expects a data source URL, reconstruct it as:

```text
collection://<uuid>
```

## Field Mapping

If the user's database fields differ from the default schema, add a `field_map` object rather than renaming the user's Notion database:

```json
{
  "field_map": {
    "tasks": {
      "任务": "Name",
      "日期": "When"
    },
    "daily_pulse": {
      "名称": "Title"
    },
    "schedule": {
      "名称": "Plan",
      "下一步行动": "Next"
    }
  }
}
```

When a mapping exists, use mapped property names for Notion reads and writes, but keep the default names in reasoning and reports.

## Validation

Before running Daily Pulse against live Notion data:

1. Confirm the JSON parses.
2. Confirm `topics_config_path` exists.
3. Fetch each configured data source.
4. If `query_data_sources` fails because the workspace lacks Enterprise + Notion AI, keep `notion_read_mode` as `search_fetch`.
5. Verify each required property exists or has a field mapping.
6. Run a dry morning brief with a small test dataset.
