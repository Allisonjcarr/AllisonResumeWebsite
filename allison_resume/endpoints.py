import json
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")
with open("resume.json") as f:
    resume_data = json.load(f)


@router.get("/resume", response_class=JSONResponse)
async def get_resume():
    return resume_data


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "resume_data": resume_data,
        },
    )


@router.get("/project-website", response_class=HTMLResponse)
async def project_website(request: Request):
    return templates.TemplateResponse(
        "project-website.html",
        {
            "request": request,
            "resume_data": resume_data,
        },
    )
