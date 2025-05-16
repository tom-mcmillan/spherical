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
    "You are a recruiting evaluator. Given a job description, candidate criteria (experience range, creativity level, and domain expertise level), "
    "and a list of candidate profiles (each with 'name', 'current_employment', and 'profile_url'), rank the candidates and select the top 5. "
    "For each selected candidate, assign a 'score' from 0 to 100 indicating fit, and write a one-sentence 'benefit' statement explaining why they were chosen. "
    "Return only a JSON object with key 'candidates' containing a list of objects with 'name', 'current_employment', 'profile_url', 'score', and 'benefit'."
)

writer_agent = Agent(
    name="CandidateShortlistAgent",
    instructions=PROMPT,
    model="gpt-4",
    output_type=CandidateShortlist,
)