from fastapi import FastAPI
from app.api.v1 import auth, leads, agents, conversations, knowledge, customers, jobs, invoices, voice
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

from fastapi import WebSocket, WebSocketDisconnect
from app.ws.manager import manager
from app.ws.voice import voice_websocket_handler
from uuid import UUID

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws/v1/realtime/{business_id}")
async def websocket_endpoint(websocket: WebSocket, business_id: str):
    try:
        b_id = UUID(business_id)
        await manager.connect(websocket, b_id)
        while True:
            await websocket.receive_text() # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, b_id)
    except Exception:
        await websocket.close()

@app.websocket("/ws/voice")
async def voice_ws_endpoint(websocket: WebSocket):
    """Twilio ConversationRelay WebSocket endpoint for AI voice calls."""
    await voice_websocket_handler(websocket)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(leads.router, prefix=f"{settings.API_V1_STR}/leads", tags=["leads"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/agents", tags=["agents"])
app.include_router(conversations.router, prefix=f"{settings.API_V1_STR}/conversations", tags=["conversations"])
app.include_router(knowledge.router, prefix=f"{settings.API_V1_STR}/knowledge", tags=["knowledge"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["customers"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])
app.include_router(invoices.router, prefix=f"{settings.API_V1_STR}/invoices", tags=["invoices"])
app.include_router(voice.router, prefix=f"{settings.API_V1_STR}/voice", tags=["voice"])
