# Source Notes

This document tracks candidate job data sources for the Data Engineering Skills Pipeline project.

## MVP Goal
Start with 1-2 sources that are:
- easy to access
- stable enough for repeated collection
- reasonably structured
- acceptable from a usage and rate-limit perspective

## Candidate Sources

### 1. Public sample or exported datasets
Pros:
- easiest to start with
- no scraping complexity
- good for pipeline scaffolding

Cons:
- less realistic than live ingestion
- may not reflect current job demand

Use case:
- ideal for initial development and debugging

### 2. Company career pages
Pros:
- often structured HTML or JSON
- useful for targeted ingestion

Cons:
- site structure varies by company
- lower volume unless many companies are covered

Use case:
- good for controlled ingestion experiments

### 3. Job APIs or feeds
Pros:
- cleaner and more repeatable than ad hoc scraping
- often easier to normalize

Cons:
- may require auth, quotas, or paid access
- availability varies

Use case:
- best long-term source if available

## Recommended Approach
1. keep the current sample JSON workflow for local validation
2. add one live-source ingestion script with a pluggable connector design
3. document assumptions and rate-limit considerations for each source

## Data Source Evaluation Criteria
- accessibility
- legal/terms-of-use comfort
- schema consistency
- volume and coverage
- ease of debugging
- repeatability

## Next Decision
Choose one live source and document:
- access method
- expected fields
- refresh frequency
- known limitations
