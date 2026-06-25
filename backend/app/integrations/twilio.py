from twilio.rest import Client
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class TwilioIntegration:
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, phone_number: Optional[str] = None):
        self.account_sid = account_sid or settings.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or settings.TWILIO_AUTH_TOKEN
        self.from_phone = phone_number or settings.TWILIO_PHONE_NUMBER
        self.enabled = False
        
        if self.account_sid and self.auth_token and self.account_sid != "mock-sid":
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
            logger.info("Twilio integration enabled.")
        else:
            logger.warning("Twilio credentials not set. Running in mock mode.")

    async def send_sms(self, to: str, body: str) -> Dict[str, Any]:
        if not self.enabled:
            logger.info(f"MOCK: Sending SMS to {to}: {body}")
            return {"sid": f"SM_mock_{to[-8:]}", "status": "sent"}

        try:
            message = self.client.messages.create(
                body=body,
                from_=self.from_phone,
                to=to
            )
            return {"sid": message.sid, "status": message.status}
        except Exception as e:
            logger.error(f"Twilio send_sms error: {e}")
            raise

    async def handle_incoming(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processes incoming webhook from Twilio."""
        return {
            "from": form_data.get("From"),
            "body": form_data.get("Body"),
            "sid": form_data.get("MessageSid")
        }

    def configure_voice_webhook(self, voice_url: str) -> Dict[str, Any]:
        """
        Update the inbound voice webhook for our Twilio phone number.
        
        Args:
            voice_url: The public URL that Twilio should POST to on inbound calls.
                       Should point to our /api/v1/voice/inbound endpoint.
        
        Returns:
            Dict with the phone number SID and status.
        """
        if not self.enabled:
            logger.info(f"MOCK: Would configure voice webhook for {self.from_phone} -> {voice_url}")
            return {"phone_number_sid": "PN_mock", "voice_url": voice_url, "status": "mock"}

        try:
            # Find the incoming phone number resource
            phone_numbers = self.client.incoming_phones.list(phone_number=self.from_phone)
            if not phone_numbers:
                logger.error(f"Phone number {self.from_phone} not found in Twilio account")
                return {"error": "Phone number not found"}

            phone_number = phone_numbers[0]
            
            # Update the voice URL and HTTP method
            updated = self.client.incoming_phones(phone_number.sid).update(
                voice_url=voice_url,
                voice_method="POST"
            )
            
            logger.info(f"Updated voice webhook for {self.from_phone}: {updated.voice_url}")
            return {
                "phone_number_sid": updated.sid,
                "voice_url": updated.voice_url,
                "voice_method": updated.voice_method,
                "status": "configured"
            }
        except Exception as e:
            logger.error(f"Failed to configure voice webhook: {e}")
            raise

    def get_phone_number_details(self) -> Optional[Dict[str, Any]]:
        """Get details about our Twilio phone number."""
        if not self.enabled:
            return {"phone_number": self.from_phone, "status": "mock"}

        try:
            phone_numbers = self.client.incoming_phones.list(phone_number=self.from_phone)
            if not phone_numbers:
                return None
            
            pn = phone_numbers[0]
            return {
                "sid": pn.sid,
                "phone_number": pn.phone_number,
                "voice_url": pn.voice_url,
                "voice_method": pn.voice_method,
                "sms_url": pn.sms_url,
                "friendly_name": pn.friendly_name,
            }
        except Exception as e:
            logger.error(f"Failed to get phone number details: {e}")
            return None
