"""
Voice API — Twilio inbound call webhook + ConversationRelay integration.

Endpoints:
  POST /api/v1/voice/inbound      — Returns TwiML with <Connect><ConversationRelay>
                                      pointing to our /ws/voice WebSocket endpoint.
  POST /api/v1/voice/configure     — Updates the Twilio phone number webhook to
                                      point to our inbound endpoint.
  GET  /api/v1/voice/status        — Shows current phone number webhook config.
"""

import logging
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from app.core.config import settings
from app.integrations.twilio import TwilioIntegration

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# System prompt for Wade's Concrete AI agent
# ---------------------------------------------------------------------------
WADES_CONCRETE_SYSTEM_PROMPT = """\
You are the ServAI virtual assistant representing Wade's Concrete. You answer \
inbound phone calls and hold natural, helpful conversations with callers.

## Business context
- **Business**: Wade's Concrete — concrete flatwork, foundations, driveways, \
sidewalks, and now expanding into high-end patio design (stamped & stained \
concrete, outdoor living spaces).
- **Owner**: Wade — phone (256) 531-6424.
- **ServAI capabilities**: lead capture, quoting, scheduling, invoicing, \
reputation management, follow-up automation.

## Your role
1. Answer questions about Wade's Concrete services, service area, and process.
2. Capture the caller's name, phone number, and project details when relevant.
3. Offer to schedule a free estimate or quote.
4. If the caller wants to speak to Wade directly, offer to transfer or have \
Wade call them back.
5. Be helpful, warm, and concise — this is a phone conversation, not an essay.

## Tone
Professional, confident, Southern-friendly. NOT robotic. Use contractions, \
natural speech patterns, and brief responses suitable for a voice call. \
Avoid jargon. Avoid long lists — keep it conversational.

## Welcome greeting (use when the call starts)
"Hey, thanks for calling back. This is ServAI. I was hoping you'd call — \
I've got some exciting things to share about what we can do for Wade's \
Concrete and those high-end patio projects you're looking at. What questions \
do you have for me?"
"""


@router.post("/inbound", summary="Twilio inbound voice webhook")
async def inbound_voice(request: Request) -> Response:
    """
    Twilio calls this endpoint when someone dials our Twilio number.
    Returns TwiML that connects the caller to our ConversationRelay WebSocket,
    where OpenAI powers the real-time conversation.
    """
    # Log incoming call metadata
    form_data = await request.form()
    from_number = form_data.get("From", "unknown")
    call_sid = form_data.get("CallSid", "unknown")
    logger.info(f"Inbound call from {from_number}, CallSid={call_sid}")

    # Build the WebSocket URL that ConversationRelay will connect to.
    # We derive it from the request's base URL so it's always correct
    # regardless of deployment (localhost, staging, production).
    base_url = str(request.base_url).rstrip("/")
    # Convert http(s) to ws(s) for the WebSocket URL
    ws_url = base_url.replace("https://", "wss://").replace("http://", "ws://")
    ws_url = f"{ws_url}/ws/voice"

    logger.info(f"Connecting ConversationRelay to WebSocket: {ws_url}")

    # Build TwiML Response with ConversationRelay
    # ConversationRelay opens a WebSocket to our server and streams
    # real-time audio + transcription for AI-driven conversation.
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay url="{ws_url}" voice="Polly.Matthew" welcomeGreeting="Hey, thanks for calling back. This is ServAI. I was hoping you'd call — I've got some exciting things to share about what we can do for Wade's Concrete and those high-end patio projects you're looking at. What questions do you have for me?"/>
  </Connect>
</Response>"""

    return Response(content=twiml, media_type="application/xml")


class ConfigureWebhookRequest(BaseModel):
    """Request body for configuring the Twilio voice webhook."""
    voice_url: str  # Public URL for the inbound voice endpoint


@router.post("/configure", summary="Configure Twilio voice webhook")
async def configure_voice_webhook(request: Request):
    """
    Updates the Twilio phone number's voice webhook to point to our
    /api/v1/voice/inbound endpoint.
    
    If voice_url is not provided in the body, it's derived from the request.
    """
    twilio = TwilioIntegration()

    # Derive the public voice URL from the request
    base_url = str(request.base_url).rstrip("/")
    default_voice_url = f"{base_url}/api/v1/voice/inbound"

    voice_url = default_voice_url

    result = twilio.configure_voice_webhook(voice_url)
    
    return {
        "message": "Voice webhook configuration updated",
        "voice_url": voice_url,
        "result": result
    }


@router.get("/status", summary="Get Twilio phone number status")
async def voice_status():
    """Returns the current webhook configuration for our Twilio phone number."""
    twilio = TwilioIntegration()
    details = twilio.get_phone_number_details()
    
    return {
        "phone_number": settings.TWILIO_PHONE_NUMBER,
        "webhook_config": details
    }
