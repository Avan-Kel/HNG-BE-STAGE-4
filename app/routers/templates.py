from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models import Template
from app.schemas import TemplateCreate, TemplateResponse, TemplateRenderRequest
from app.render_engine import render_template

router = APIRouter(prefix="/api/v1/templates", tags=["Templates"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a template
@router.post("/", response_model=TemplateResponse)
def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    existing = db.query(Template).filter(
        Template.template_code == template.template_code,
        Template.version == template.version
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Template with this code and version already exists")

    db_template = Template(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

# List all templates
@router.get("/", response_model=List[TemplateResponse])
def list_templates(db: Session = Depends(get_db)):
    return db.query(Template).all()

# Get latest version of a template by code
@router.get("/{template_code}", response_model=TemplateResponse)
def get_template(template_code: str, db: Session = Depends(get_db)):
    template = db.query(Template).filter(
        Template.template_code == template_code
    ).order_by(Template.version.desc()).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return template

# Render template
@router.post("/render", response_model=dict)
def render(tpl_req: TemplateRenderRequest, db: Session = Depends(get_db)):
    tpl = db.query(Template).filter(
        Template.template_code == tpl_req.template_code
    ).order_by(Template.version.desc()).first()

    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")

    subject, body = render_template(tpl.subject, tpl.body, tpl_req.variables)

    return {
        "success": True,
        "data": {"subject": subject, "body": body},
        "message": "rendered",
        "meta": None
    }

# Delete a single template by code + version
@router.delete("/{template_code}/{version}", response_model=dict)
def delete_template(template_code: str, version: int, db: Session = Depends(get_db)):
    template = db.query(Template).filter(
        Template.template_code == template_code,
        Template.version == version
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(template)
    db.commit()

    return {
        "success": True,
        "message": f"Template {template_code} v{version} deleted",
        "data": None,
        "meta": None
    }

# Delete ALL templates
@router.delete("/", response_model=dict)
def delete_all_templates(db: Session = Depends(get_db)):
    db.query(Template).delete()
    db.commit()

    return {
        "success": True,
        "message": "All templates deleted",
        "data": None,
        "meta": None
    }
