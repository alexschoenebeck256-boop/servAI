from typing import Dict, Any, Optional
from app.agents.base import BaseAgent
from app.models.models import Lead, LeadStatus

class SalesAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action")
        
        if action == "qualify_lead":
            lead_id = task_data.get("lead_id")
            lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                # Real qualification logic using LLM
                prompt = f"Analyze this lead: {lead.customer_name}, {lead.phone}, {lead.email}. Service needed: {lead.service_type}. Determine if it is a high-priority lead."
                summary = await self.ask_llm(prompt)
                
                lead.status = LeadStatus.QUALIFYING
                lead.summary = summary
                self.db.commit()
                
                # Send welcome SMS via Twilio
                from app.integrations.twilio import TwilioIntegration
                twilio = TwilioIntegration()
                await twilio.send_sms(lead.phone, f"Hi {lead.customer_name}, this is the team at ServAI. We received your request for {lead.service_type} and are reviewing it now!")
                
                result = {"status": "success", "summary": summary}
            else:
                result = {"status": "error", "message": "Lead not found."}
        else:
            result = {"status": "error", "message": f"Unsupported action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        
        # Use RAG to get pricing/services context
        kb_context = await self.get_context(message)
        
        system_prompt = f"You are a Sales AI Agent. Use the following context to help book jobs:\n{kb_context}"
        response = await self.ask_llm(message, system_prompt=system_prompt)
        
        self.status = "IDLE"
        return response
