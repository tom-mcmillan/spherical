from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a recruiting assistant. Given a job description and candidate criteria (experience range, creativity level, and domain expertise level), "
    "propose 5 to 10 LinkedIn search queries. For each search, output an object with keys 'query' (the LinkedIn search string) and 'reason' (a brief rationale). "
    "Return your result as a JSON object with key 'searches' containing a list of these objects."
)


class CandidateSearchItem(BaseModel):
    query: str
    "The LinkedIn search query string."

    reason: str
    "A brief rationale for why this search query is relevant."


class CandidateSearchPlan(BaseModel):
    searches: list[CandidateSearchItem]
    "A list of LinkedIn search queries and their reasons."


planner_agent = Agent(
    name="CandidatePlannerAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=CandidateSearchPlan,
)