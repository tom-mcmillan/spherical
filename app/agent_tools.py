import os
import json
import requests
import openai
from agents import function_tool
from typing import List, Dict, Any
from .settings import COMPANY_DESCRIPTION
import logging

logger = logging.getLogger("candidate_finder.agent_tools")
from .prompts import (
    PARSE_INTENT_PROMPT,
    CSE_QUERY_TEMPLATE,
    SCORE_CANDIDATES_PROMPT,
    JUSTIFY_CANDIDATES_PROMPT,
)

# Parse the intent from the job description using LLM
@function_tool(
    name_override="parse_intent",
    description_override=PARSE_INTENT_PROMPT,
    strict_mode=False,
)
async def parse_intent_fn(job_description: str) -> Dict[str, Any]:
    logger.debug("parse_intent called; job_description length=%d", len(job_description))
    prompt = PARSE_INTENT_PROMPT.format(job_description=job_description)
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": COMPANY_DESCRIPTION},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0,
    )
    return json.loads(resp.choices[0].message.content)

# Find candidate LinkedIn profiles using Google CSE
@function_tool(
    name_override="find_candidates",
    description_override="Search for candidate LinkedIn profiles via Google CSE",
    strict_mode=False,
)
async def find_candidates_fn(role: str, skills: List[str], location: str) -> List[Dict[str, Any]]:
    logger.debug(
        "find_candidates called; role=%s, skills=%s, location=%s",
        role,
        skills,
        location,
    )
    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    engine_id = os.getenv("GOOGLE_CSE_ENGINE_ID")
    candidates: List[Dict[str, Any]] = []
    if api_key and engine_id:
        query = CSE_QUERY_TEMPLATE.format(role=role)
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": engine_id, "q": query},
            timeout=5,
        )
        items = resp.json().get("items", [])
        for item in items[:5]:
            name = item.get("title", "").split("|")[0].strip()
            link = item.get("link", "")
            candidates.append({"name": name, "profile_url": link})
    # Fallback to hard-coded candidates
    if not candidates:
        logger.warning("find_candidates: no results from Google CSE; using fallback candidates")
        candidates = [
            {"name": "Alice Smith", "profile_url": "https://www.linkedin.com/in/alicesmith"},
            {"name": "Bob Johnson", "profile_url": "https://www.linkedin.com/in/bobjohnson"},
            {"name": "Carol Lee", "profile_url": "https://www.linkedin.com/in/carollee"},
        ]
    return candidates

# Score candidates by fit using LLM
@function_tool(
    name_override="score_candidates",
    description_override=SCORE_CANDIDATES_PROMPT,
    strict_mode=False,
)
async def score_candidates_fn(candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
    logger.debug("score_candidates called; scoring %d candidates", len(candidates))
    prompt = SCORE_CANDIDATES_PROMPT.format(
        role_desc=job_description,
        candidates_list=json.dumps(candidates),
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": COMPANY_DESCRIPTION},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0,
    )
    return json.loads(resp.choices[0].message.content)

# Justify candidates by generating benefit statements with LLM
@function_tool(
    name_override="justify_candidates",
    description_override=JUSTIFY_CANDIDATES_PROMPT,
    strict_mode=False,
)
async def justify_candidates_fn(candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
    logger.debug("justify_candidates called; explaining %d candidates", len(candidates))
    results: List[Dict[str, Any]] = []
    for c in candidates:
        name = c.get("name", "")
        prompt = JUSTIFY_CANDIDATES_PROMPT.format(
            role_desc=job_description,
            candidate_name=name,
        )
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": COMPANY_DESCRIPTION},
                {"role": "user", "content": prompt},
            ],
            max_tokens=60,
            temperature=0.7,
        )
        benefit = resp.choices[0].message.content.strip()
        results.append({"name": name, "profile_url": c.get("profile_url"), "benefit": benefit})
    return results

tools = [
    parse_intent_fn,
    find_candidates_fn,
    score_candidates_fn,
    justify_candidates_fn,
]