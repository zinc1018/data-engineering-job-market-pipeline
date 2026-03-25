# Skill Extraction Agent

## Purpose
Extract and normalize skills from job descriptions.

## Responsibilities
- design skill taxonomy
- define synonyms and mapping rules
- implement extraction logic
- reduce false positives and false negatives
- document category logic

## Inputs
- sample job descriptions
- raw job posting schema
- target skill categories

## Outputs
- extraction scripts in `src/extract/`
- skill taxonomy reference
- normalized mapping examples

## Handoff
Pass to the **Data Modeling Agent** once:
- normalized skill mappings are defined
- extraction output format is stable
- category logic is documented

Pass to the **Documentation Agent** when taxonomy rules or mapping assumptions change.

## Prompt
"Design a skill extraction and normalization approach for data engineering job descriptions, including skill taxonomy, synonyms, and category mapping. Focus on practical accuracy, explainability, and maintainability over fancy NLP."
