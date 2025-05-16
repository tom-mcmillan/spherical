# Configuration

## Environment Variables

- **OPENAI_API_KEY**: Your OpenAI API key for GPT-4 model calls.
- **GOOGLE_CSE_API_KEY**: Google Custom Search JSON API key.
- **GOOGLE_CSE_ENGINE_ID**: Google Custom Search engine ID.

Copy `.env.example` to `.env` and fill in these variables before running.

## Company Description

The company description is version-controlled in `src/config.py` under `COMPANY_DESCRIPTION`. You can override it at runtime by setting the `COMPANY_DESCRIPTION` environment variable, but the default should suffice in most cases.