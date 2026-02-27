import asyncio
from typing import Dict, Any
from .agents import ExistentialistAgent, AdvaitaAgent, ModeratorAgent

existentialist = ExistentialistAgent()
advaita = AdvaitaAgent()
moderator = ModeratorAgent()

async def run_parallel_mode(session_id: str, message: str) -> Dict[str, str]:
    # Run agents in parallel
    results = await asyncio.gather(
        existentialist.get_response(session_id, message),
        advaita.get_response(session_id, message)
    )
    return {
        "existentialist": results[0],
        "advaita": results[1]
    }

async def run_debate_mode(session_id: str, message: str) -> Dict[str, str]:
    # Existentialist Input
    ex_response = await existentialist.get_response(session_id, message)

    # Advaita Rebuttal - responding to Existentialist
    ad_rebuttal = await advaita.get_response(session_id, f"The Existentialist just said: '{ex_response}'. What is your rebuttal from the Advaita perspective?")

    # Existentialist Counter
    ex_counter = await existentialist.get_response(session_id, f"The Advaita philosopher responded to you with: '{ad_rebuttal}'. What is your counter-argument?")

    # Moderator Synthesis
    synthesis_prompt = (
        f"Original Topic: {message}\n"
        f"Existentialist initially said: {ex_response}\n"
        f"Advaita Rebuttal: {ad_rebuttal}\n"
        f"Existentialist Counter: {ex_counter}\n"
        "Please synthesize these views."
    )
    mod_synthesis = await moderator.get_response(session_id, synthesis_prompt)

    return {
        "existentialist": ex_response,
        "advaita_rebuttal": ad_rebuttal,
        "existentialist_counter": ex_counter,
        "moderator_synthesis": mod_synthesis
    }
