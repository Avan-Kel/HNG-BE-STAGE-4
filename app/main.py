from fastapi import FastAPI
from app.database import Base, engine
from app.routers import templates

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Template Service API")

# Include routers
app.include_router(templates.router)

@app.get("/")
def root():
    return {"message": "Template Service is running successfully"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

