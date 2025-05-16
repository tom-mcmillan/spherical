# Agent Tools

The candidate-finder pipeline uses four function-based tools defined in `src/agent_tools.py`. Each is decorated with the OpenAI Agents SDK's `@function_tool`:

1. **parse_intent** (`parse_intent_fn`) — Extracts `role`, `skills`, and `location` from the job description.
2. **find_candidates** (`find_candidates_fn`) — Calls Google CSE to retrieve LinkedIn profiles (falls back to hard-coded list).
3. **score_candidates** (`score_candidates_fn`) — Uses GPT-4 to assign a fit score (0–100) and returns a sorted list.
4. **justify_candidates** (`justify_candidates_fn`) — Uses GPT-4 to write a persuasive benefit statement per candidate.

To extend:

- Create a new async function in `src/agent_tools.py`.
- Decorate it with `@function_tool(name_override=..., description_override=...)`.
- Add it to the `tools` list at the bottom of `agent_tools.py`.