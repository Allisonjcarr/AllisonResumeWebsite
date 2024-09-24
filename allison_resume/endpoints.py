import json

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .chart_data import get_chart_data
from .dependencies import log_visit
from .models import WebsiteVisits
from .db import get_session_local, SessionLocal

from sqlalchemy import func

router = APIRouter()
templates = Jinja2Templates(directory="templates")
with open("resume.json") as f:
    resume_data = json.load(f)


@router.get("/resume", response_class=JSONResponse)
async def get_resume(visit=Depends(log_visit)):
    return resume_data


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    db: SessionLocal = Depends(get_session_local),
    visit: WebsiteVisits = Depends(log_visit),
):
    total_visits = db.query(WebsiteVisits).count()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "resume_data": resume_data,
            "total_visits": total_visits,
        },
    )


@router.get("/project-website", response_class=HTMLResponse)
async def project_website(
    request: Request,
    db: SessionLocal = Depends(get_session_local),
    visit: WebsiteVisits = Depends(log_visit),
):
    chart_data = get_chart_data(db)

    return templates.TemplateResponse(
        "project-website.html",
        {
            "request": request,
            "resume_data": resume_data,
            "chart_data": chart_data,
        },
    )
