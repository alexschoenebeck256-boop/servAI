import stripe
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class StripeIntegration:
    def __init__(self, api_key: Optional[str] = None):
        # The lead requested STRIPE_SECRET_KEY, but config.py has STRIPE_API_KEY.
        # I'll stick to settings.STRIPE_API_KEY as per config.py, 
        # or use STRIPE_SECRET_KEY if specifically provided in env.
        self.api_key = api_key or settings.STRIPE_SECRET_KEY
        self.enabled = False
        if self.api_key and self.api_key != "mock-key":
            stripe.api_key = self.api_key
            self.enabled = True
            logger.info("Stripe integration enabled.")
        else:
            logger.warning("Stripe API key not set. Running in mock mode.")

    async def create_customer(self, email: str, name: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.enabled:
            logger.info(f"MOCK: Creating Stripe customer for {email}")
            return {"id": f"cus_mock_{email[:8]}", "email": email, "name": name}
        
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata
            )
            return customer
        except Exception as e:
            logger.error(f"Stripe create_customer error: {e}")
            raise

    async def create_invoice(self, customer_id: str, amount: int, description: str, currency: str = "usd") -> Dict[str, Any]:
        """Amount in cents."""
        if not self.enabled:
            logger.info(f"MOCK: Creating Stripe invoice for {customer_id}: {amount} {currency}")
            return {"id": f"in_mock_{customer_id[-8:]}", "amount": amount, "status": "draft"}

        try:
            # Create an invoice item first
            stripe.InvoiceItem.create(
                customer=customer_id,
                amount=amount,
                currency=currency,
                description=description,
            )
            # Create the invoice
            invoice = stripe.Invoice.create(
                customer=customer_id,
                auto_advance=True # Automatically finalize and begin collection
            )
            return invoice
        except Exception as e:
            logger.error(f"Stripe create_invoice error: {e}")
            raise

    async def handle_webhook(self, payload: str, sig_header: str, webhook_secret: str) -> Dict[str, Any]:
        if not self.enabled:
            logger.info("MOCK: Handling Stripe webhook")
            return {"status": "mock_success"}

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        except Exception as e:
            logger.error(f"Stripe webhook error: {e}")
            raise
