# Ingestion Agent

## Purpose
Design and implement the raw job posting ingestion layer.

## Responsibilities
- evaluate data sources
- implement source collection logic
- capture raw records reliably
- log ingestion runs
- handle source-specific normalization

## Inputs
- `PROJECT_PLAN.md`
- target job sources
- raw schema expectations

## Outputs
- ingestion scripts in `src/ingest/`
- sample raw data in `data/raw/`
- source notes in `docs/`

## Handoff
Pass to the **Skill Extraction Agent** once:
- raw sample job postings exist
- raw schema is stable enough to parse
- source limitations are documented

Pass to the **Documentation Agent** when ingestion assumptions, source coverage, or storage format changes.

## Prompt
"Design and implement the raw job posting ingestion layer for the Data Engineering Skills Pipeline project. Prefer reliable and simple collection methods first. Document assumptions, source limitations, and how raw data is stored."
