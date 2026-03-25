# AGENTS.md - Data Engineering Skills Pipeline

This project already has a working MVP, so the agent model should reflect ongoing improvement work rather than initial scaffolding. Keep the agent system simple: each agent should own a clear responsibility and produce concrete artifacts.

## Recommended Agent Set

### 1. Planner Agent
**Purpose:** Break the project into milestones, tasks, and dependencies.

**Owns:**
- project roadmap
- milestone sequencing
- task breakdown
- priorities
- scope control

**Outputs:**
- milestone plan
- weekly task list
- implementation backlog

**When to use:**
- at project start
- before each new milestone
- when scope starts drifting

---

### 2. Ingestion Agent
**Purpose:** Build and maintain job posting collection workflows.

**Owns:**
- source evaluation
- API or scraping logic
- raw data capture
- ingestion logging
- source-specific normalization

**Outputs:**
- ingestion scripts
- source connectors
- raw job posting files/tables
- ingestion run notes

**Main concerns:**
- reliability
- rate limits
- duplicate records
- source schema differences

---

### 3. Skill Extraction Agent
**Purpose:** Extract and normalize skills from job descriptions.

**Owns:**
- skill dictionary design
- keyword matching logic
- normalization rules
- category mapping
- extraction quality review

**Outputs:**
- skill taxonomy
- extraction scripts
- normalized skill mappings
- false positive/false negative notes

**Main concerns:**
- messy text
- synonyms
- overmatching
- undermatching

---

### 4. Data Modeling Agent
**Purpose:** Design analytics-ready tables and transformation logic.

**Owns:**
- schema design
- staging models
- mart models
- table relationships
- SQL transformations

**Outputs:**
- data model definitions
- SQL models
- dbt models if used
- documentation for tables and fields

**Main concerns:**
- clean naming
- maintainability
- analytical usefulness
- reproducibility

---

### 5. Data Quality Agent
**Purpose:** Validate that the pipeline output is trustworthy.

**Owns:**
- quality checks
- schema validation
- duplicate detection
- null checks
- basic pipeline test coverage

**Outputs:**
- test cases
- validation scripts
- quality rules
- issue reports

**Main concerns:**
- missing values
- duplicate jobs
- broken transformations
- inconsistent skill mappings

---

### 6. Documentation Agent
**Purpose:** Keep the project understandable and portfolio-ready.

**Owns:**
- README
- architecture docs
- data dictionary
- setup instructions
- resume/interview summaries

**Outputs:**
- repo documentation
- architecture narrative
- onboarding notes
- polished project summary

**Main concerns:**
- clarity
- completeness
- professionalism
- keeping docs in sync with code

---

## Recommended Core Working Set
For this repository's current state, use these 6 agents as the default operating set:

1. **Planner Agent**
2. **Ingestion Agent**
3. **Skill Extraction Agent**
4. **Data Modeling Agent**
5. **Data Quality Agent**
6. **Documentation Agent**

This is the right balance for a live PostgreSQL pipeline that already includes mart logic, target-role filtering, quality checks, and dashboard exports.

---

## Lean Version
If you want to keep it lean for a narrow task, use only these 4 agents:

1. **Planner Agent**
2. **Ingestion Agent**
3. **Data Modeling Agent**
4. **Documentation Agent**

---

## Best Practical Setup for This Project
Recommended working set:

- **Planner Agent** -> decides what to build next
- **Ingestion Agent** -> collects single-board and multi-board raw postings
- **Skill Extraction Agent** -> identifies and normalizes skills from live job descriptions
- **Data Modeling Agent** -> builds staging, marts, and target-role views
- **Data Quality Agent** -> protects against broken reruns, bad dates, orphaned facts, and drift
- **Documentation Agent** -> keeps the repo portfolio-ready

---

## Suggested Execution Order
### Phase 1 - Setup
- Planner Agent
- Documentation Agent

### Phase 2 - Raw Data Collection
- Ingestion Agent

### Phase 3 - Skill Normalization
- Skill Extraction Agent

### Phase 4 - Transformations
- Data Modeling Agent
- Data Quality Agent

### Phase 5 - Portfolio Polish and Reporting
- Documentation Agent

---

## Recommended Deliverables Per Agent
### Planner Agent
- `PROJECT_PLAN.md`
- milestone checklist
- prioritized backlog

### Ingestion Agent
- `src/ingest/`
- source notes in `docs/`
- sample raw data in `data/raw/`

### Skill Extraction Agent
- `src/extract/`
- skill mapping reference
- extraction test examples

### Data Modeling Agent
- `sql/staging/`
- `sql/marts/`
- transformation notes in `docs/data_dictionary.md`

### Data Quality Agent
- `tests/`
- validation logic
- data quality checklist

### Documentation Agent
- `README.md`
- `docs/architecture.md`
- interview/resume-ready summary

---

## Suggested Agent Prompts

### Planner Agent Prompt
"Break the next iteration of the Data Engineering Skills Pipeline project into practical tasks and dependencies. Prioritize improvements to live ingestion, role filtering, extraction quality, mart usefulness, and portfolio presentation."

### Ingestion Agent Prompt
"Design and improve the raw Greenhouse ingestion layer for the Data Engineering Skills Pipeline project. Prefer reliable public-board collection, clear normalization, and repeatable loading behavior."

### Skill Extraction Agent Prompt
"Improve the skill extraction and normalization approach for data engineering job descriptions, focusing on practical accuracy, explainability, and reduced false positives."

### Data Modeling Agent Prompt
"Improve the staging and mart layer for job postings and extracted skills so the data is analytics-ready, supports cross-company comparisons, and is easy to explain in interviews."

### Data Quality Agent Prompt
"Define and implement data quality checks for raw jobs, transformed jobs, and extracted skills. Focus on duplicates, missing values, invalid mappings, rerun safety, and mart integrity."

### Documentation Agent Prompt
"Write clear, professional documentation for the current working pipeline, including README, architecture summary, setup instructions, role-filter logic, and portfolio-facing outcomes."

---

## My Recommendation
Use these 6 by default:
- Planner Agent
- Ingestion Agent
- Skill Extraction Agent
- Data Modeling Agent
- Data Quality Agent
- Documentation Agent

That is the right balance of structure without turning the repo into process overhead.
