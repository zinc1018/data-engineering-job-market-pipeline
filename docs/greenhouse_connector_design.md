# Greenhouse Connector Design

## Why Greenhouse
Greenhouse is a strong v1 live-source target because many companies expose public job listings through a relatively consistent API-backed structure. That makes it easier to build a reusable connector pattern than scraping highly variable job board pages.

## Design Goal
Create a connector that:
- fetches public job postings for one company board token
- maps jobs into the project's normalized raw schema
- saves output to JSON first for validation
- can later feed directly into PostgreSQL loading

## Initial Scope
### Inputs
- `BOARD_TOKEN` environment variable
  - example concept: a company-specific Greenhouse board token

### Output
A JSON file containing normalized records with these fields:
- `source`
- `source_job_id`
- `title`
- `company`
- `location`
- `description`
- `job_url`
- `posted_date`

## File Layout
- `src/ingest/greenhouse_connector.py`
- `src/ingest/fetch_greenhouse_job_postings.py`
- `tests/test_greenhouse_connector.py`

## Connector Flow
1. Read `BOARD_TOKEN`
2. Call the public Greenhouse jobs endpoint with `content=true`
3. Parse returned jobs
4. Map each job into `JobPostingRecord`
5. Save normalized records to `data/raw/greenhouse_job_postings.json`
6. Later: reuse the existing raw loader to insert into PostgreSQL

## Mapping Notes
### Source
- format: `greenhouse:<board_token>`

### Source Job ID
- use Greenhouse job `id`

### Company
- for MVP, use the board token as company identifier
- later, enrich with actual company name if needed

### Description
- map from Greenhouse `content`
- keep raw HTML/text handling simple in MVP

### Posted Date
- not always guaranteed in a uniform field
- attempt to extract from metadata when present
- allow null if unavailable

## Advantages
- cleaner than large job boards
- reusable across multiple company tokens
- easier to explain in interviews as a connector pattern
- fits the agent-driven ingestion design already created

## Future Enhancements
- support multiple board tokens in one run
- filter for data-related roles before saving
- strip HTML from descriptions if needed
- push records directly into PostgreSQL
- add retry handling and structured logging
