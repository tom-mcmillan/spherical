# Prompt Templates

All default prompt templates live in `src/prompts.py`:

- **PARSE_INTENT_PROMPT**: Extracts `role`, `skills`, and `location` from free-form job descriptions.
- **CSE_QUERY_TEMPLATE**: Formats the Google Custom Search query (e.g. `{role} site:linkedin.com/in`).
- **SCORE_CANDIDATES_PROMPT**: Ranks candidate fit (0–100) given a job description and candidate list.
- **BENEFIT_PROMPT_TEMPLATE** (alias `JUSTIFY_CANDIDATES_PROMPT`): Generates a one-sentence benefit statement per candidate.

To customize, edit the corresponding constant in `src/prompts.py` and restart the service.