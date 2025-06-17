from sqlalchemy import Column, String, Boolean, JSON
from app.db.base import Base

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True, index=True)
    business_id = Column(String, index=True)  # Привязка к бизнесу
    name = Column(String)
    content = Column(JSON)  # HTML/Jinja2 шаблон
    styles = Column(JSON)   # CSS/стили
    is_default = Column(Boolean, default=False)