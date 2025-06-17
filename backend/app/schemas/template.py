from pydantic import BaseModel
from typing import Dict, Any

class TemplateCreate(BaseModel):
    name: str
    business_id: str
    content: Dict[str, Any]  # Структура шаблона
    styles: Dict[str, Any]   # Стили
    is_default: bool = False

class TemplateResponse(TemplateCreate):
    id: str