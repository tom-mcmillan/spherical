from pydantic import BaseModel
from agents import Agent
from ...agent_tools import get_profile_data_fn

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
    "  • A list of candidate profiles (each with 'name', 'current_employment', and 'profile_url')\n"
    "You have access to a tool named get_profile_data that takes a 'profile_url' and returns detailed profile_data as JSON.\n"
    "First, for each candidate, call get_profile_data(profile_url) to retrieve profile_data.\n"
    "Exclude any candidates whose profile_data indicates they are likely full-time employees not open to consulting opportunities.\n"
    "Then, from the remaining candidates, rank them by fit to the criteria and select the top 5.\n"
    "For each selected candidate, assign a 'score' (0–100) and write a one-sentence 'benefit' statement explaining why they were chosen.\n"
    "Return only a JSON object with key 'candidates' containing a list of objects with 'name', 'current_employment', 'profile_url', 'score', and 'benefit'."
)

writer_agent = Agent(
    name="CandidateShortlistAgent",
    instructions=PROMPT,
    model="gpt-4o",
    # Provide the get_profile_data tool for enriching LinkedIn profiles
    tools=[get_profile_data_fn],
    output_type=CandidateShortlist,
)