from typing import List, Dict
from .config import client, OPENAI_MODEL

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
    # Keep the system message if it exists
    system_msg = history[0] if history and history[0]["role"] == "system" else None

    messages_to_summarize = history[1:] if system_msg else history

    prompt = "Summarize the following conversation history concisely while preserving the key philosophical points discussed:\n\n"
    for msg in messages_to_summarize:
        prompt += f"{msg['role']}: {msg['content']}\n"

    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content

        new_history = []
        if system_msg:
            new_history.append(system_msg)
        new_history.append({"role": "system", "content": f"Previous conversation summary: {summary}"})

        sessions[session_id][agent_name] = new_history
        print(f"Summarized history for session {session_id}, agent {agent_name}")
    except Exception as e:
        print(f"Error during summarization: {e}")

def get_history(session_id: str, agent_name: str) -> List[Dict[str, str]]:
    return sessions.get(session_id, {}).get(agent_name, [])
