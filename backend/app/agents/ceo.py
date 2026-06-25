from typing import Dict, Any, Optional
from app.agents.base import BaseAgent
from app.models.models import Lead, Job, Business
from sqlalchemy import func

class CEOAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action", "generate_report")
        
        if action == "generate_report":
            # Real KPI monitoring
            lead_count = self.db.query(Lead).filter(Lead.business_id == self.business_id).count()
            job_count = self.db.query(Job).filter(Job.business_id == self.business_id).count()
            
            # Aggregate revenue
            revenue = self.db.query(func.sum(Job.total_amount)).filter(Job.business_id == self.business_id, Job.status == "COMPLETED").scalar() or 0
            
            prompt = f"""
            You are the CEO AI for a home service business. 
            Here are the current KPIs:
            - Total Leads: {lead_count}
            - Completed Jobs: {job_count}
            - Total Revenue: ${revenue:,.2f}
            
            Generate a concise executive summary and 3 strategic recommendations for the business owner.
            """
            
            report_content = await self.ask_llm(prompt)
            
            result = {
                "summary": report_content,
                "kpis": {
                    "leads": lead_count,
                    "jobs": job_count,
                    "revenue": float(revenue)
                }
            }
        else:
            result = {"error": f"Unknown action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        
        system_prompt = "You are the CEO AI Agent for a home service business. Your goal is to provide strategic insights and manage operations."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        
        self.status = "IDLE"
        return response
