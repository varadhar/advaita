# Existentialism vs. Advaita Multi-Agent Chatbot

This is a multi-agent web application that facilitates philosophical dialogues between an Existentialist Agent, an Advaita Vedanta Agent, and a Moderator Agent.

## Features
- **Parallel Response Mode**: Both agents respond to the user input simultaneously.
- **Advanced Debate Mode**: A structured debate flow (Existentialist -> Advaita -> Existentialist -> Moderator).
- **Session Management**: UUID-based sessions with in-memory conversation history.
- **Auto-summarization**: Conversation history is summarized after 30 messages to maintain context window efficiency.

## Tech Stack
- **Backend**: FastAPI, Python 3.11+, OpenAI GPT-4o-mini.
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Fetch API).

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r multi_agent_chatbot/requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` in the root directory and add your OpenAI API Key.
   ```bash
   cp multi_agent_chatbot/.env.example .env
   # Edit .env with your key
   ```

3. **Run the Backend**:
   ```bash
   uvicorn multi_agent_chatbot.backend.main:app --host 0.0.0.0 --port 8000
   ```

4. **Access the Frontend**:
   Open `multi_agent_chatbot/frontend/index.html` in your web browser.

## API Examples

### Get Session ID
```bash
curl http://localhost:8000/session
```

### Chat (Parallel Mode)
```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the meaning of life?", "mode": "parallel", "session_id": "your-uuid"}'
```

### Chat (Debate Mode)
```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Does the self exist?", "mode": "debate", "session_id": "your-uuid"}'
```
