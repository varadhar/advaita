from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from .orchestrator import run_parallel_mode, run_debate_mode

app = FastAPI(title="Existentialism vs. Advaita Multi-Agent App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    mode: str  # "parallel" or "debate"
    session_id: str = None

@app.get("/session")
async def get_session():
    return {"session_id": str(uuid.uuid4())}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.session_id:
        request.session_id = str(uuid.uuid4())

    try:
        if request.mode == "parallel":
            responses = await run_parallel_mode(request.session_id, request.message)
            return {"session_id": request.session_id, "mode": "parallel", "data": responses}
        elif request.mode == "debate":
            responses = await run_debate_mode(request.session_id, request.message)
            return {"session_id": request.session_id, "mode": "debate", "data": responses}
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Choose 'parallel' or 'debate'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
