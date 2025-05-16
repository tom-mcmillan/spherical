import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from .settings import COMPANY_DESCRIPTION, SYSTEM_PROMPT
from .agent_tools import tools
from agents import Agent, Runner
load_dotenv()

import logging

logger = logging.getLogger("candidate_finder")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI()

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.post("/process")
async def process(request: Request):
    logger.info("POST /process called")
    # Parse request payload
    payload = await request.json()
    job_desc = payload.get("request")
    if not job_desc:
        return JSONResponse({"error": "No job description provided"}, status_code=400)

    # Collect user criteria for context
    context = {
        "job_description": job_desc,
        "creativity": payload.get("creativity", 0),
        "hospitality_expertise": payload.get("hospitality_expertise", 0),
        "experience": payload.get("experience", 0),
    }

    # If required API keys (OpenAI + Google CSE) are not all configured, return hard-coded fallback
    if not (
        os.getenv("OPENAI_API_KEY")
        and os.getenv("GOOGLE_CSE_API_KEY")
        and os.getenv("GOOGLE_CSE_ENGINE_ID")
    ):
        logger.warning(
            "Missing API keys for OpenAI or Google CSE; returning fallback candidates"
        )
        fallback = [
            {"name": "Alice Smith", "profile_url": "https://www.linkedin.com/in/alicesmith"},
            {"name": "Bob Johnson", "profile_url": "https://www.linkedin.com/in/bobjohnson"},
            {"name": "Carol Lee", "profile_url": "https://www.linkedin.com/in/carollee"},
        ]
        # Include empty benefit statements for compatibility
        candidates = [
            {"name": c["name"], "profile_url": c["profile_url"], "benefit": ""}
            for c in fallback
        ]
        return JSONResponse({"candidates": candidates})

    # Run the agent pipeline
    try:
        logger.info("Running agent pipeline")
        agent = Agent(
            name="CandidateFinderAgent",
            instructions=SYSTEM_PROMPT,
            tools=tools,
            tool_use_behavior={"stop_at_tool_names": ["justify_candidates"]},
        )
        result = await Runner.run(
            starting_agent=agent,
            input=job_desc,
            context=context,
        )
        candidates = result.final_output or []
    except Exception:
        logger.exception(
            "Error during agent pipeline; falling back to default candidates"
        )
        # On any error, fall back to basic candidates with empty benefits
        fallback = [
            {"name": "Alice Smith", "profile_url": "https://www.linkedin.com/in/alicesmith"},
            {"name": "Bob Johnson", "profile_url": "https://www.linkedin.com/in/bobjohnson"},
            {"name": "Carol Lee", "profile_url": "https://www.linkedin.com/in/carollee"},
        ]
        candidates = [
            {"name": c["name"], "profile_url": c["profile_url"], "benefit": ""}
            for c in fallback
        ]
    # Return structured JSON list of candidates
    return JSONResponse({"candidates": candidates})
 
@app.get("/healthz")
async def healthz():
    """
    Health check endpoint. Verifies required environment variables are set.
    """
    missing = []
    for var in ("OPENAI_API_KEY", "GOOGLE_CSE_API_KEY", "GOOGLE_CSE_ENGINE_ID"):
        if not os.getenv(var):
            missing.append(var)
    if missing:
        logger.error("Healthz check failed; missing env vars: %s", missing)
        return JSONResponse({"status": "error", "missing": missing}, status_code=503)
    logger.info("Healthz check passed")
    return JSONResponse({"status": "ok"})