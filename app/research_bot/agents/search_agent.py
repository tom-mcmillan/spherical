from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings
from pydantic import BaseModel

class CandidateProfile(BaseModel):
    name: str
    current_employment: str
    profile_url: str

class CandidateProfileList(BaseModel):
    candidates: list[CandidateProfile]

INSTRUCTIONS = (
    "You are a recruiting assistant. Given a LinkedIn search query, use the provided WebSearchTool to perform the search. "
    "Then parse the search results to identify up to 5 candidate profiles. Each profile should include:\n"
    "- name (full name)\n"
    "- current_employment (job title and company)\n"
    "- profile_url (LinkedIn URL)\n"
    "Return your result as a JSON object with key 'candidates' containing a list of these profiles."
)

search_agent = Agent(
    name="CandidateSearchAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=CandidateProfileList,
)