from main import app
from src.controllers.job_controller import (
    get_jobs,
    get_job_by_id,
    create_job,
    update_job,
    delete_job,
)

BASE_PATH = "/api/job"


@app.get(f"{BASE_PATH}")
async def get_jobs_route(request):
    return get_jobs()


@app.get(f"{BASE_PATH}/<job_id>")
async def get_job_by_id_route(request, job_id):
    return get_job_by_id(job_id)


@app.post(f"{BASE_PATH}")
async def create_job_route(request):
    return create_job(request.json)


@app.patch(f"{BASE_PATH}/<job_id>")
async def update_job_route(request, job_id):
    return update_job(job_id, request.json)


@app.delete(f"{BASE_PATH}/<job_id>")
async def delete_job_route(request, job_id):
    return delete_job(job_id)
