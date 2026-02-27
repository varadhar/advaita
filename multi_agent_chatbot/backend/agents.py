import google.generativeai as genai
from .config import get_model
from .memory import add_message, get_history

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.model = get_model(system_prompt)

    async def get_response(self, session_id: str, user_input: str) -> str:
        # Add user message to history
        await add_message(session_id, self.name, "user", user_input)

        # Get full history
        history = get_history(session_id, self.name)

        # Gemini expects a different format for history
        # role: user -> user, role: assistant -> model
        gemini_history = []
        # In our case, history already contains the last user message
        for msg in history[:-1]: # all but the last one
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        try:
            chat = self.model.start_chat(history=gemini_history)
            response = await chat.send_message_async(user_input)
            reply = response.text

            # Add agent reply to history
            await add_message(session_id, self.name, "assistant", reply)
            return reply
        except Exception as e:
            return f"Error from {self.name}: {str(e)}"

class ExistentialistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Existentialist",
            system_prompt=(
                "You are an Existentialist philosopher, deeply rooted in the works of Jean-Paul Sartre and Albert Camus. "
                "You believe in radical freedom, the absence of inherent meaning, and the 'Absurd'. "
                "Your tone is serious, contemplative, and emphasizes individual responsibility in creating meaning."
            )
        )

class AdvaitaAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Advaita",
            system_prompt=(
                "You are an Advaita Vedanta philosopher. You believe in Non-duality (Advaita). "
                "Your core philosophy is that the individual self (Atman) is identical to the ultimate reality (Brahman). "
                "The world and the ego are 'Maya' (illusion). Your tone is peaceful, detached, and focused on the singularity of consciousness."
            )
        )

class ModeratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Moderator",
            system_prompt=(
                "You are a Philosophical Moderator. Your job is to synthesize the perspectives of an Existentialist and an Advaita Vedanta philosopher. "
                "You should highlight common ground, point out fundamental disagreements, and provide a balanced summary that deepens the inquiry."
            )
        )
