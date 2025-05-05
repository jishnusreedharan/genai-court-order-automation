from pydantic import BaseModel
from typing import Optional

class AgentState(BaseModel):
    file_path: str
    document_text: Optional[str] = None
    national_id: Optional[str] = None
    action: Optional[str] = None
    customer_id: Optional[str] = None
    outcome: Optional[str] = None
