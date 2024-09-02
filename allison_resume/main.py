import json
import os


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

with open("resume.json") as f:
    resume_data = json.load(f)


@app.get("/resume", response_class=JSONResponse)
async def get_resume():
    return resume_data


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "resume_data": resume_data,
        },
    )


@app.get("/project-website", response_class=HTMLResponse)
async def project_website(request: Request):
    return templates.TemplateResponse(
        "project-website.html",
        {
            "request": request,
            "resume_data": resume_data,
        },
    )
