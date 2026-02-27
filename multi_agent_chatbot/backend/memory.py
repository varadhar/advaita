from typing import List, Dict
import google.generativeai as genai
from .config import GEMINI_MODEL_NAME

# In-memory storage: {session_id: {agent_name: [messages]}}
sessions: Dict[str, Dict[str, List[Dict[str, str]]]] = {}

SUMMARIZATION_TRIGGER = 30

async def add_message(session_id: str, agent_name: str, role: str, content: str):
    if session_id not in sessions:
        sessions[session_id] = {}
    if agent_name not in sessions[session_id]:
        sessions[session_id][agent_name] = []

    sessions[session_id][agent_name].append({"role": role, "content": content})

    if len(sessions[session_id][agent_name]) >= SUMMARIZATION_TRIGGER:
        await summarize_history(session_id, agent_name)

async def summarize_history(session_id: str, agent_name: str):
    history = sessions[session_id][agent_name]

    prompt = "Summarize the following conversation history concisely while preserving the key philosophical points discussed:\n\n"
    for msg in history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = await model.generate_content_async(prompt)
        summary = response.text

        # In Gemini version, we replace the history with a system-like summary message
        # Note: Gemini doesn't have a strict 'system' role in the same way for every message,
        # but we can use 'user' with a specialized instruction or just keep it in our internal state.
        # We'll keep it as 'system' role in our internal list and handle it in agents.py

        new_history = [{"role": "system", "content": f"Previous conversation summary: {summary}"}]

        sessions[session_id][agent_name] = new_history
        print(f"Summarized history for session {session_id}, agent {agent_name}")
    except Exception as e:
        print(f"Error during summarization: {e}")

def get_history(session_id: str, agent_name: str) -> List[Dict[str, str]]:
    return sessions.get(session_id, {}).get(agent_name, [])
