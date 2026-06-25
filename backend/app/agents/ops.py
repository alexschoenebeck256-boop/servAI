from typing import Dict, Any, Optional
from app.agents.base import BaseAgent

class OpsAgent(BaseAgent):
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "WORKING"
        action = task_data.get("action", "optimize_schedules")
        
        if action == "optimize_schedules":
            # Real logic: Look at pending jobs and available technicians
            from app.models.models import Job, User
            pending_jobs = self.db.query(Job).filter(Job.business_id == self.business_id, Job.status == "PENDING").all()
            technicians = self.db.query(User).filter(User.business_id == self.business_id, User.role == "TECHNICIAN").all()
            
            prompt = f"""
            You are the Operations Manager AI for a home service business.
            Task: Optimize schedules for {len(pending_jobs)} pending jobs and {len(technicians)} technicians.
            
            Pending Jobs: {[{"id": j.id, "type": j.job_type} for j in pending_jobs]}
            Technicians: {[{"id": t.id, "name": t.full_name} for t in technicians]}
            
            Provide a dispatching plan and any routing optimizations.
            """
            plan = await self.ask_llm(prompt)
            result = {"status": "success", "plan": plan}
        else:
            result = {"error": f"Unknown action: {action}"}
            
        self.status = "IDLE"
        return result

    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.status = "WORKING"
        system_prompt = "You are an Ops AI Agent. Your goal is to manage dispatching and technician schedules."
        response = await self.ask_llm(message, system_prompt=system_prompt)
        self.status = "IDLE"
        return response
