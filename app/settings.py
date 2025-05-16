import os
from dotenv import load_dotenv

load_dotenv()
import openai  # Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "")

from .config import COMPANY_DESCRIPTION as DEFAULT_COMPANY_DESCRIPTION
COMPANY_DESCRIPTION = os.getenv("COMPANY_DESCRIPTION", DEFAULT_COMPANY_DESCRIPTION)

# System prompt guiding the overall agent pipeline (injects company description)
from .prompts import SYSTEM_PROMPT_TEMPLATE
SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(COMPANY_DESCRIPTION=COMPANY_DESCRIPTION)