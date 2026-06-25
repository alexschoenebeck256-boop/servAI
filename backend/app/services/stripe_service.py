import os
import httpx
from typing import Dict, Any, Optional

class StripeService:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_API_KEY", "mock-stripe-key")
        self.base_url = "https://api.stripe.com/v1"

    async def create_payment_intent(self, amount: int, currency: str = "usd") -> Dict[str, Any]:
        """Create a payment intent in Stripe."""
        print(f"MOCK Stripe: Creating payment intent for {amount} {currency}")
        return {"id": "pi_mock_123", "client_secret": "mock_secret_456"}

    async def create_invoice(self, customer_id: str, amount: int) -> Dict[str, Any]:
        """Create and send an invoice in Stripe."""
        print(f"MOCK Stripe: Creating invoice for customer {customer_id} for {amount}")
        return {"id": "in_mock_123", "status": "draft"}

stripe_service = StripeService()
