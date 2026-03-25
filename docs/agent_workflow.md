# Agent Workflow

This document explains when to use each agent and how work should flow through the project.

## Recommended Core Agents
- Planner Agent
- Ingestion Agent
- Skill Extraction Agent
- Data Modeling Agent
- Data Quality Agent
- Documentation Agent

## Formal Handoff Chain
1. **Planner Agent / BA** -> defines scope, requirements, milestones, KPIs, and the next highest-value tasks
2. **Ingestion Agent** -> collects and stores raw job posting data
3. **Skill Extraction Agent** -> extracts and normalizes skill data from raw job descriptions
4. **Data Modeling Agent** -> transforms raw and extracted data into analytics-ready models
5. **Data Quality Agent** -> validates mart integrity, rerun safety, and pipeline trustworthiness
6. **Documentation Agent** -> updates docs, architecture, setup, and portfolio-facing materials
7. **Planner Agent / BA** -> reviews progress, resolves gaps, and plans the next cycle

This loop should repeat for each milestone.

## Entry and Exit Criteria
| Agent | Entry Criteria | Exit Criteria | Handoff To |
|---|---|---|---|
| Planner Agent / BA | Project exists and needs direction, scope definition, or milestone planning | MVP scope, requirements, success criteria, KPIs, and prioritized tasks are clear | Ingestion Agent |
| Ingestion Agent | Target sources and raw data expectations are defined | Raw sample postings are collected and raw schema is stable enough to parse | Skill Extraction Agent |
| Skill Extraction Agent | Sample job descriptions and raw schema are available | Skill taxonomy, mappings, and extraction output format are stable | Data Modeling Agent |
| Data Modeling Agent | Raw jobs and extracted skills are available | Staging, marts, and target-role views support core analytics questions | Data Quality Agent |
| Data Quality Agent | Mart tables and views exist | Quality checks and tests cover key integrity risks | Documentation Agent |
| Documentation Agent | Project artifacts or design decisions changed | Docs are current, understandable, and portfolio-ready | Planner Agent / BA |

## Workflow by Phase

### Phase 1: Project Setup
**Primary agents:** Planner Agent, Documentation Agent

Goals:
- confirm MVP scope
- define milestones
- establish repo structure
- create initial docs

Outputs:
- `PROJECT_PLAN.md`
- `README.md`
- implementation backlog

---

### Phase 2: Raw Data Collection
**Primary agent:** Ingestion Agent

Goals:
- select public Greenhouse boards
- implement collection logic
- save raw job postings
- document source limitations

Outputs:
- scripts in `src/ingest/`
- sample files in `data/raw/`
- ingestion notes

Exit criteria:
- at least 50 postings collected from a live source
- raw schema is stable enough to build against

---

### Phase 3: Skill Extraction
**Primary agent:** Skill Extraction Agent

Goals:
- define skill taxonomy
- map synonyms to normalized skills
- parse job descriptions
- validate extraction quality on samples

Outputs:
- extraction logic in `src/extract/`
- skill taxonomy reference
- sample mappings

Exit criteria:
- extracted skills are usable for modeling
- common DE tools are consistently recognized

---

### Phase 4: Data Modeling
**Primary agent:** Data Modeling Agent

Goals:
- create staging models
- create mart models
- create filtered target-role analytical views
- define key relationships
- document field meanings

Outputs:
- SQL models in `sql/staging/`
- SQL models in `sql/marts/`
- updated data dictionary

Exit criteria:
- analytics-ready tables exist
- core metrics and cross-company comparisons can be queried from the model

---

### Phase 5: Quality, Documentation, and Portfolio Polish
**Primary agents:** Data Quality Agent, Documentation Agent

Goals:
- validate rerun safety
- validate integrity of marts and target-role views
- update README
- document architecture
- explain design decisions
- produce resume/interview-ready summaries

Outputs:
- quality checks
- polished docs
- setup instructions
- architecture narrative

Exit criteria:
- repo is understandable to a recruiter or hiring manager
- project is easy to demo and explain
- live outputs can be trusted

## Operating Rules
1. Planner Agent decides what comes next.
2. Ingestion Agent should keep raw data unchanged as much as possible.
3. Skill Extraction Agent should prioritize explainable rules over complex models.
4. Data Modeling Agent should optimize for clarity and analytics usefulness.
5. Data Quality Agent should be part of normal iteration, not a late add-on.
6. Documentation Agent should update docs whenever structure or logic changes.

## Suggested Working Rhythm
- Start each session with Planner Agent
- Use one or two build agents for the active phase
- Run Data Quality Agent before closing substantial work
- End with Documentation Agent updating project artifacts

## Suggested Immediate Next Steps
1. Improve target-role filtering precision
2. Expand skill taxonomy and synonym coverage
3. Add more portfolio-facing dashboard summaries
4. Add integration-style tests for database outputs
5. Document live results and tradeoffs
