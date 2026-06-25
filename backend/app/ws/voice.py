"""
Voice WebSocket handler — Twilio ConversationRelay + OpenAI real-time conversation.

Twilio ConversationRelay opens a WebSocket to /ws/voice when an inbound call
is answered. It streams:
  - Transcribed user speech as text messages
  - DTMF digits
  - Call lifecycle events (setup, interrupt, end)

We respond with:
  - Text that ConversationRelay speaks back to the caller via TTS (Polly.Matthew)

The AI brain is OpenAI GPT-4, called via the existing LLM provider.
"""

import json
import logging
import asyncio
from typing import Optional
from fastapi import WebSocket, WebSocketDisconnect
from app.llm.provider import get_llm_provider
from app.api.v1.voice import WADES_CONCRETE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class VoiceSession:
    """Manages a single voice call session with OpenAI conversation history."""

    def __init__(self, call_sid: Optional[str] = None):
        self.call_sid = call_sid
        self.conversation_history: list[dict] = [
            {"role": "system", "content": WADES_CONCRETE_SYSTEM_PROMPT}
        ]
        self.llm = get_llm_provider(provider_name="openai", model="gpt-4o")
        self._lock = asyncio.Lock()

    async def get_ai_response(self, user_text: str) -> str:
        """Send user text to OpenAI and return the AI's response."""
        async with self._lock:
            self.conversation_history.append({"role": "user", "content": user_text})

            try:
                response = await self.llm.complete(
                    self.conversation_history,
                    temperature=0.7,
                    max_tokens=300,  # Keep responses short for voice
                )
                self.conversation_history.append({"role": "assistant", "content": response})
                # Trim history to prevent token overflow (keep system + last 20 messages)
                if len(self.conversation_history) > 22:
                    self.conversation_history = (
                        [self.conversation_history[0]] + self.conversation_history[-20:]
                    )
                return response
            except Exception as e:
                logger.error(f"OpenAI API error during voice call: {e}")
                # Fallback response so the call doesn't go silent
                return "I'm sorry, I'm having a little trouble right now. Could you repeat that?"


# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------

async def voice_websocket_handler(websocket: WebSocket) -> None:
    """
    Handles the Twilio ConversationRelay WebSocket session.

    Protocol (ConversationRelay v1):
    - Incoming messages are JSON with a "type" field:
        - "setup"       — session init (contains callSid, etc.)
        - "prompt"      — transcribed user speech (text in "voice_prompt")
        - "interrupt"   — user interrupted the AI's speech
        - "dtmf"        — DTMF digit pressed
        - "end"         — call ended
    - Outgoing messages we send:
        - {"type": "response", "text": "...", "session_id": "..."}
        - {"type": "end"}  — to hang up
    """
    await websocket.accept()
    session: Optional[VoiceSession] = None
    session_id: Optional[str] = None

    logger.info("Voice WebSocket connection accepted (ConversationRelay)")

    try:
        while True:
            raw = await websocket.receive_text()
            logger.debug(f"ConversationRelay message: {raw[:200]}")

            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from ConversationRelay: {raw[:100]}")
                continue

            msg_type = msg.get("type", "")

            # ---- Setup ----
            if msg_type == "setup":
                session_id = msg.get("session_id", "unknown")
                call_sid = msg.get("call_sid") or msg.get("callSid")
                session = VoiceSession(call_sid=call_sid)
                logger.info(
                    f"Voice session setup: session_id={session_id}, call_sid={call_sid}"
                )
                # No immediate response — the welcomeGreeting in TwiML handles intro
                continue

            # ---- User speech transcription ----
            elif msg_type == "prompt":
                if session is None:
                    logger.warning("Received prompt before setup, creating session")
                    session = VoiceSession()
                    session_id = "late-init"

                user_text = msg.get("voice_prompt", msg.get("text", ""))
                if not user_text.strip():
                    continue

                logger.info(f"Caller said: {user_text}")

                # Get AI response
                ai_response = await session.get_ai_response(user_text)
                logger.info(f"AI responds: {ai_response}")

                # Send response back to ConversationRelay for TTS
                response_msg = {
                    "type": "response",
                    "text": ai_response,
                }
                if session_id:
                    response_msg["session_id"] = session_id

                await websocket.send_text(json.dumps(response_msg))

            # ---- User interrupted AI speech ----
            elif msg_type == "interrupt":
                logger.info("Caller interrupted AI speech — stopping playback")
                # ConversationRelay handles playback stop; we just log it.
                # No response needed — wait for the next prompt.

            # ---- DTMF ----
            elif msg_type == "dtmf":
                digit = msg.get("digit", "")
                logger.info(f"DTMF digit: {digit}")
                # We could add IVR logic here. For now, treat as user input.
                if session:
                    ai_response = await session.get_ai_response(
                        f"The caller pressed the {digit} key on their phone."
                    )
                    response_msg = {
                        "type": "response",
                        "text": ai_response,
                    }
                    if session_id:
                        response_msg["session_id"] = session_id
                    await websocket.send_text(json.dumps(response_msg))

            # ---- Call ended ----
            elif msg_type == "end":
                logger.info(f"Voice call ended: session_id={session_id}")
                break

            else:
                logger.warning(f"Unknown ConversationRelay message type: {msg_type}")

    except WebSocketDisconnect:
        logger.info(f"Voice WebSocket disconnected: session_id={session_id}")
    except Exception as e:
        logger.error(f"Voice WebSocket error: {e}")
    finally:
        if session:
            logger.info(
                f"Voice session ended — call_sid={session.call_sid}, "
                f"messages exchanged={len(session.conversation_history) - 1}"
            )
