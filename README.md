# Template Service 

The **Template Service** is a standalone microservice responsible for storing, versioning, and rendering reusable notification templates used by email and push services in the Distributed Notification System.

It supports:
- Create templates  
- Get template by code  
- List all templates  
- Version history  
- Delete templates  
- Render template with variables  
- Deployable with Docker or Railway  
- CI/CD using GitHub Actions & Railway

---

## 🚀 Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Deployment | Railway / Docker |
| CI/CD | GitHub Actions |


## Features Implemented

✔ Store templates with metadata  
✔ Multiple versions of each template  
✔ Render template by replacing variables (`{{name}}`, `{{link}}`, etc.)  
✔ Soft delete templates  
✔ Pagination response format  
✔ Environment variable DB connection  
✔ Ready for CI/CD deployment  
✔ Exposed REST API


## Start server
uvicorn app.main:app --reload

## Using Docker
docker build -t template-service .
docker run -p 8000:8000 --env-file .env template-service


## Create Template
POST /api/v1/templates/
{
  "template_code": "welcome_email",
  "subject": "Welcome!",
  "body": "Hello {{name}}, welcome onboard!"
}

## Render Template
POST /api/v1/templates/render
{
  "template_code": "welcome_email",
  "version": 1,
  "variables": {
    "name": "KC"
  }
}
