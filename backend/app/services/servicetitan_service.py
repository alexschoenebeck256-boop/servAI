import os
import httpx
from typing import Dict, Any, List, Optional

class ServiceTitanService:
    def __init__(self):
        self.client_id = os.getenv("SERVICETITAN_CLIENT_ID", "mock-client-id")
        self.client_secret = os.getenv("SERVICETITAN_CLIENT_SECRET", "mock-secret")
        self.tenant_id = os.getenv("SERVICETITAN_TENANT_ID", "mock-tenant-id")
        self.api_key = os.getenv("SERVICETITAN_API_KEY", "mock-api-key")
        self.base_url = "https://api.servicetitan.io"

    async def get_jobs(self, business_id: str) -> List[Dict[str, Any]]:
        """Fetch jobs from ServiceTitan."""
        print(f"MOCK ServiceTitan: Fetching jobs for tenant {self.tenant_id}")
        return [
            {"id": "job_1", "status": "Scheduled", "customer": "John Doe"},
            {"id": "job_2", "status": "In Progress", "customer": "Jane Smith"},
        ]

    async def create_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job in ServiceTitan."""
        print(f"MOCK ServiceTitan: Creating job with data: {job_data}")
        return {"id": "job_new_123", "status": "Success"}

servicetitan_service = ServiceTitanService()
