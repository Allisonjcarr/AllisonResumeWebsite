import json
from datetime import datetime

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from .dependencies import log_visit
from .models import WebsiteVisits
from .db import get_session_local, SessionLocal
from pytz import timezone
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
    total_visits = db.query(WebsiteVisits).count()
    visits = db.query(WebsiteVisits).order_by(WebsiteVisits.id.desc()).limit(10).all()

    visit_times = (
        db.query(WebsiteVisits.visited_at).order_by(WebsiteVisits.visited_at).all()
    )
    visit_times = [visit[0].strftime("%Y-%m-%d %H:%M:%S") for visit in visit_times]

    return templates.TemplateResponse(
        "project-website.html",
        {
            "request": request,
            "resume_data": resume_data,
            "total_visits": total_visits,
            "visits": visits,
            "visit_times": visit_times,
        },
    )


@router.get("/charts/visits-over-time", response_class=HTMLResponse)
async def visits_over_time(
    request: Request,
    db: SessionLocal = Depends(get_session_local),
    visit: WebsiteVisits = Depends(log_visit),
):
    # Use SQLite-compatible strftime to group visits by hour
    visits_by_hour = (
        db.query(
            func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at).label("hour"),
            func.count(WebsiteVisits.id).label("visit_count"),
        )
        .group_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .order_by(func.strftime("%Y-%m-%d %H", WebsiteVisits.visited_at))
        .all()
    )

    # Prepare the data for the chart
    est_timezone = timezone("US/Eastern")
    visit_dates = []
    visit_data = []

    for visit in visits_by_hour:
        # Parse the string into a datetime object
        utc_time = datetime.strptime(visit.hour, "%Y-%m-%d %H")

        # Localize the datetime object to UTC and convert to EST
        est_time = timezone("UTC").localize(utc_time).astimezone(est_timezone)

        # Format the time in EST as 'YYYY-MM-DD HH:00'
        formatted_time = est_time.strftime("%m/%d/%Y %I:%M %p")

        visit_dates.append(formatted_time)
        visit_data.append(visit.visit_count)

    return templates.TemplateResponse(
        "charts/visits-over-time.html",
        {
            "request": request,
            "title": "Visits over time",
            "visit_dates": visit_dates,  # Time labels for x-axis (hourly)
            "visit_data": visit_data,  # Number of visits per hour (y-axis)
        },
    )
