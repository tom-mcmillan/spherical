"""
Manager orchestrating the research bot workflow: plan → search → write.
"""
import os
import requests
import urllib.parse
from agents import Runner
from .agents.planner_agent import CandidateSearchPlan, planner_agent
from .agents.search_agent import search_agent
from .agents.writer_agent import writer_agent


class ResearchManager:
    """
    A manager that orchestrates planning, searching, and report writing using agents.
    """
    async def run(self, description: str, creativity: float, domain_expertise: float, experience: int) -> list[dict]:
        """
        Orchestrate candidate search: plan LinkedIn queries, perform searches, and shortlist candidates.
        """
        # Step 1: Plan LinkedIn search queries based on description and criteria
        plan_prompt = (
            f"Job description: {description}\n"
            f"Experience range (years): {experience} to {experience + 2}\n"
            f"Creativity level (0.0-1.0): {creativity}\n"
            f"Domain expertise level (0.0-1.0): {domain_expertise}"
        )
        plan_result = await Runner.run(planner_agent, plan_prompt)
        search_plan = plan_result.final_output_as(CandidateSearchPlan)

        # Step 2: Execute each LinkedIn search and gather profiles
        profiles = []
        for item in search_plan.searches:
            try:
                search_input = f"Search query: {item.query}\nReason: {item.reason}"
                search_result = await Runner.run(search_agent, search_input)
                profiles.extend(search_result.final_output.candidates)
            except Exception:
                continue

        # Deduplicate by profile URL
        unique_profiles = list({p.profile_url: p for p in profiles}.values())

        # Step 3 & 4: Shortlist and rank candidates using the writer agent with enrichment tool
        # Pass raw profiles; the writer_agent can call get_profile_data to enrich each candidate
        raw_profiles = [p.dict() for p in unique_profiles]
        shortlist_prompt = (
            f"Job description: {description}\n"
            f"Experience range (years): {experience} to {experience + 2}\n"
            f"Creativity level (0.0-1.0): {creativity}\n"
            f"Domain expertise level (0.0-1.0): {domain_expertise}\n"
            f"Candidates: {raw_profiles}"
        )
        shortlist_result = await Runner.run(writer_agent, shortlist_prompt)
        # Return the shortlisted candidates as plain dicts
        return [c.dict() for c in shortlist_result.final_output.candidates]