import os
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.rag.service import get_rag_service

class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db
        self.rag = get_rag_service(db)

    async def upload_document(self, business_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Ingest a document into the business's vector knowledge base."""
        # Note: In a real implementation, we'd chunk the text, call an embedding model, and store in pgvector/Chroma
        print(f"MOCK Knowledge: Ingesting document for business {business_id}")
        # await self.rag.add_document(business_id, content, metadata)
        return {"status": "success", "message": "Document ingested."}

    async def search_knowledge(self, business_id: str, query: str) -> List[Dict[str, Any]]:
        """Search the business's knowledge base."""
        return await self.rag.search(business_id, query)

def get_knowledge_service(db: Session) -> KnowledgeService:
    return KnowledgeService(db)
