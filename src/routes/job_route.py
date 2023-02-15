from main import app
from src.controllers.job_controller import get_jobs, get_job_by_id
from sanic.response import json

BASE_PATH = "/api/job"


@app.get(f"{BASE_PATH}")
async def get_jobs_route(request):
    return get_jobs()


@app.get(f"{BASE_PATH}/<job_id>")
async def get_job_by_id_route(request, job_id):
    return get_job_by_id(job_id)
