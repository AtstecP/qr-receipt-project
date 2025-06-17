from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.template import TemplateCreate, TemplateResponse
from app.models.template import Template
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=TemplateResponse)
def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    """Создание нового шаблона квитанции"""
    db_template = Template(
        name=template.name,
        business_id=template.business_id,
        content=template.content,
        styles=template.styles,
        is_default=template.is_default
    )
    db.add(db_template)
    db.commit()
    return db_template

@router.get("/{business_id}", response_model=list[TemplateResponse])
def get_templates(business_id: str, db: Session = Depends(get_db)):
    """Получение всех шаблонов для бизнеса"""
    return db.query(Template).filter(Template.business_id == business_id).all()

@router.put("/set-default/{template_id}")
def set_default_template(template_id: str, db: Session = Depends(get_db)):
    """Установка шаблона по умолчанию"""
    template = db.query(Template).get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Сбрасываем все default флаги у этого бизнеса
    db.query(Template).filter(
        Template.business_id == template.business_id
    ).update({"is_default": False})
    
    # Устанавливаем новый default
    template.is_default = True
    db.commit()
    return {"message": "Default template updated"}