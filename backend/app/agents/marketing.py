from typing import Dict, Any, Optional
from app.agents.base import BaseAgent
import logging

logger = logging.getLogger(__name__)

class MarketingAgent(BaseAgent):
    """
    Marketing Agent: Manages ad campaigns, generates social media content, 
    and analyzes marketing performance.
    """
    
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        task = task_data.get("task", "general_marketing")
        
        # Real logic: Query database for context
        from app.models.models import Lead, Job
        from sqlalchemy import func
        
        lead_count = self.db.query(Lead).filter(Lead.business_id == self.business_id).count()
        job_count = self.db.query(Job).filter(Job.business_id == self.business_id).count()
        
        logger.info(f"Marketing Agent working on task: {task}")
        
        prompt = f"""
        You are the Marketing Director for a home services business.
        Business Context: {lead_count} total leads, {job_count} total jobs.
        Task: {task}
        Additional data: {task_data.get("data", {})}
        
        Provide a strategic marketing recommendation or content plan based on these performance metrics.
        """
        
        response = await self.ask_llm(prompt)
        
        self.status = "IDLE"
        return {
            "status": "success",
            "agent": "marketing",
            "metrics": {"leads": lead_count, "jobs": job_count},
            "recommendation": response
        }

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        system_prompt = "You are a Marketing AI Agent. Your goal is to help with lead generation and brand awareness."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        self.status = "IDLE"
        return response

    async def generate_ad_copy(self, platform: str, service: str) -> str:
        prompt = f"Generate high-converting {platform} ad copy for a {service} service."
        return await self.ask_llm(prompt)
