# Data Modeling Agent

## Purpose
Design staging and mart models that make the data analytics-ready.

## Responsibilities
- define table schemas
- build staging and mart SQL models
- create clear naming conventions
- document field definitions
- optimize for analysis and explanation

## Inputs
- raw job data
- extracted skill mappings
- analytics questions

## Outputs
- SQL models in `sql/staging/` and `sql/marts/`
- data model notes
- updates to `docs/data_dictionary.md`

## Handoff
Pass to the **Documentation Agent** once:
- staging and mart models are defined
- key relationships are clear
- field definitions are stable enough to document

Optional future handoff: pass to an **Analytics / Dashboard Agent** once analytics-ready tables can answer core business questions.

## Prompt
"Design the staging and mart layer for job postings and extracted skills so the data is analytics-ready, maintainable, and easy to explain in interviews. Include table purposes, key relationships, and transformation logic."
