from pydantic import BaseModel, validator
from typing import Dict, Optional
from uuid import UUID

# --------------------------
# Template creation model
# --------------------------
class TemplateCreate(BaseModel):
    code: str
    version: int
    subject: str
    body: str
    language: str

# --------------------------
# Template response model
# --------------------------
class TemplateResponse(BaseModel):
    id: str
    code: str
    version: int
    subject: str
    body: str
    language: str

    @validator("id", pre=True)
    def convert_id_to_str(cls, v):
        return str(v)  # force UUID → string

    model_config = {
        "from_attributes": True 
    }

# --------------------------
# Template render request model
# --------------------------
class TemplateRenderRequest(BaseModel):
    template_code: str
    version: Optional[int]
    variables: Dict[str, str]

