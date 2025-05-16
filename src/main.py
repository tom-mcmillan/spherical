import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from .research_bot.manager import ResearchManager
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



    # If OPENAI_API_KEY is missing, return fallback candidates
    if not os.getenv("OPENAI_API_KEY"):
        fallback = [
            {"name": "Alice Smith", "profile_url": "https://www.linkedin.com/in/alicesmith", "benefit": ""},
            {"name": "Bob Johnson", "profile_url": "https://www.linkedin.com/in/bobjohnson", "benefit": ""},
            {"name": "Carol Lee", "profile_url": "https://www.linkedin.com/in/carollee", "benefit": ""},
        ]
        return JSONResponse({"candidates": fallback})

    # Delegate to the research-bot manager for the backend workflow

    # Extract user criteria from payload
    creativity = float(payload.get("creativity", 0.0))
    domain_expertise = float(payload.get("hospitality_expertise", 0.0))
    experience = int(payload.get("experience", 0))

    manager = ResearchManager()
    try:
        candidates = await manager.run(job_desc, creativity, domain_expertise, experience)
        # Return the candidate list as JSON
        return JSONResponse({"candidates": candidates})
    except Exception:
        logger.exception("ResearchManager run failed")
        return JSONResponse({"error": "Internal server error"}, status_code=500)
 
@app.get("/healthz")
async def healthz():
    """
    Health check endpoint. Verifies required environment variables are set.
    """
    missing = []
    for var in ("OPENAI_API_KEY",):
        if not os.getenv(var):
            missing.append(var)
    if missing:
        logger.error("Healthz check failed; missing env vars: %s", missing)
        return JSONResponse({"status": "error", "missing": missing}, status_code=503)
    logger.info("Healthz check passed")
    return JSONResponse({"status": "ok"})