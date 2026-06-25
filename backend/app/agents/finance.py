from typing import Dict, Any, Optional
from app.agents.base import BaseAgent
import logging

logger = logging.getLogger(__name__)

class FinanceAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action", "process_invoices")
        
        if action == "process_invoices":
            # Real logic: Look for completed jobs without invoices
            from app.models.models import Job
            from app.integrations.stripe import StripeIntegration
            
            jobs = self.db.query(Job).filter(Job.business_id == self.business_id, Job.status == "COMPLETED", Job.stripe_invoice_id == None).all()
            stripe = StripeIntegration()
            
            results = []
            for job in jobs:
                try:
                    # In a real app, we'd find/create the customer first
                    inv = await stripe.create_invoice(
                        customer_id=f"cus_{job.customer_id}", # Placeholder
                        amount=int(job.total_amount * 100),
                        description=f"Job #{job.id}: {job.job_type}"
                    )
                    job.stripe_invoice_id = inv["id"]
                    results.append({"job_id": str(job.id), "invoice_id": inv["id"]})
                except Exception as e:
                    logger.error(f"Failed to create invoice for job {job.id}: {e}")
            
            self.db.commit()
            result = {"status": "success", "processed": results}
        else:
            result = {"error": f"Unknown action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        system_prompt = "You are a Finance AI Agent. Your goal is to manage invoicing and payments."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        self.status = "IDLE"
        return response
