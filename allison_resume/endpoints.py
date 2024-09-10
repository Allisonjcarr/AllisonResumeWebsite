import json
from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from .dependencies import log_visit
from .models import get_session_local, WebsiteVisits

router = APIRouter()
templates = Jinja2Templates(directory="templates")
with open("resume.json") as f:
    resume_data = json.load(f)


@router.get("/resume", response_class=JSONResponse)
async def get_resume(visit=Depends(log_visit)):
    return resume_data


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request, db=Depends(get_session_local), visit=Depends(log_visit)
):
    total_visits = db.query(WebsiteVisits).count()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "resume_data": resume_data, "total_visits": total_visits},
    )


@router.get("/project-website", response_class=HTMLResponse)
async def project_website(request: Request, visit=Depends(log_visit)):
    return templates.TemplateResponse(
        "project-website.html",
        {
            "request": request,
            "resume_data": resume_data,
        },
    )
