from pydantic import BaseModel
from agents import Agent

class Candidate(BaseModel):
    name: str
    current_employment: str
    profile_url: str
    score: int
    benefit: str

class CandidateShortlist(BaseModel):
    candidates: list[Candidate]

PROMPT = (
    "You are a recruiting evaluator. You receive:\n"
    "  • A job description and candidate criteria (experience range, creativity level, domain expertise level)\n"
    "  • A list of enriched candidate profiles (each with 'name', 'current_employment', 'profile_url', and 'profile_data' JSON from ScrapeCreators)\n"
    "First, exclude any candidates whose 'profile_data' indicates they are likely full-time employees not open to consulting opportunities.\n"
    "Then, from the remaining candidates, rank them by fit to the criteria and select the top 5.\n"
    "For each selected candidate, assign a 'score' (0–100) and write a one-sentence 'benefit' statement explaining why they were chosen.\n"
    "Return only a JSON object with key 'candidates' containing a list of objects with 'name', 'current_employment', 'profile_url', 'score', and 'benefit'."
)

writer_agent = Agent(
    name="CandidateShortlistAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=CandidateShortlist,
)