from typing import Dict, Any, Optional
from app.agents.base import BaseAgent
from app.models.models import Job, JobStatus

class CSAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action")
        
        if action == "follow_up":
            job_id = task_data.get("job_id")
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if job and job.status == JobStatus.COMPLETED:
                # Send feedback request via Twilio
                from app.integrations.twilio import TwilioIntegration
                twilio = TwilioIntegration()
                
                # Assume we have customer phone in the Job or Customer model
                customer_phone = job.customer_phone # Placeholder
                if customer_phone:
                    await twilio.send_sms(customer_phone, f"Hi, this is ServAI. How was your recent {job.job_type} service? Please reply with 1-5 stars!")
                    result = {"status": "success", "message": f"Feedback request sent for job {job_id}."}
                else:
                    result = {"status": "error", "message": "Customer phone number missing."}
            else:
                result = {"status": "error", "message": "Job not completed or not found."}
        else:
            result = {"status": "error", "message": f"Unsupported action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        
        system_prompt = "You are a Customer Service AI Agent. Your goal is to ensure customer satisfaction."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        
        self.status = "IDLE"
        return response
