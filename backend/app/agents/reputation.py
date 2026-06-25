from typing import Dict, Any, Optional
from app.agents.base import BaseAgent

class ReputationAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action", "monitor_reviews")
        
        if action == "monitor_reviews":
            # Real logic: Look at recent jobs and reviews
            from app.models.models import Job
            # In a real app, we'd have a Review model. Let's assume some context data for now.
            reviews = task_data.get("reviews", [])
            
            prompt = f"""
            You are the Reputation Manager AI for a home service business.
            Recent Reviews: {reviews}
            
            Analyze these reviews. For any negative reviews, draft a professional and empathetic response.
            For positive reviews, draft a thank you message.
            """
            analysis = await self.ask_llm(prompt)
            result = {"status": "success", "analysis": analysis}
        else:
            result = {"error": f"Unknown action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        system_prompt = "You are a Reputation AI Agent. Your goal is to manage reviews and business reputation."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        self.status = "IDLE"
        return response
