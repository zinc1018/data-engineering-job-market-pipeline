# Source Notes

This document tracks the current live ingestion source and its operational assumptions.

## Current Live Source
### Greenhouse public board API
Base pattern:
- `https://boards-api.greenhouse.io/v1/boards/<board_token>/jobs?content=true`

Validated board tokens:
- `airtable`
- `stripe`

## Why Greenhouse Works Well For MVP
- public and easy to access
- consistent JSON response shape across boards
- useful volume for cross-company comparison
- enough detail in job descriptions for skill extraction

## Current Field Mapping
- `id` -> `source_job_id`
- `title` -> `title`
- `company_name` -> `company`
- `location.name` -> `location`
- `content` -> `description`
- `absolute_url` -> `job_url`
- `first_published` or `updated_at` -> `posted_date`

## Known Payload Quirks
- `metadata` may be `null`
- `first_published` is more reliable than metadata for posting dates
- boards include many non-target roles, so role filtering happens downstream, not during raw ingestion

## Operational Notes
- ingestion now retries transient request failures up to 3 attempts with simple backoff
- fetched records are validated before being written to JSON
- successful runs append a JSONL log entry to `data/processed/ingestion_runs.jsonl`
- raw loading uses upsert behavior on `(source, source_job_id)`

## Current Limitations
- only Greenhouse boards are implemented as live sources
- no source-specific rate limiting beyond basic request retry
- no persisted ingestion metrics table in PostgreSQL yet

## Recommended Next Ingestion Improvements
1. Add structured ingestion metrics to PostgreSQL instead of file-only logs.
2. Add one more public source type beyond Greenhouse.
3. Add source-level tests for malformed or partial API payloads.
