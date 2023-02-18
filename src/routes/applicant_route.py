from main import app
from src.controllers.applicant_controller import (
    get_applicants,
    get_applicant_by_id,
    create_applicant,
    update_applicant,
    delete_applicant,
)

BASE_PATH = "/api/applicant"


@app.get(f"{BASE_PATH}")
def get_applicant_route(request):
    return get_applicants()


@app.get(f"{BASE_PATH}/<applicant_id>")
def get_applicant_by_id_route(request, applicant_id):
    return get_applicant_by_id(applicant_id)


@app.post(f"{BASE_PATH}")
def create_applicant_route(request):
    return create_applicant(request.json)


@app.patch(f"{BASE_PATH}/<applicant_id>")
def update_applicant_route(request, applicant_id):
    return update_applicant(applicant_id, request.json)


@app.delete(f"{BASE_PATH}/<applicant_id>")
def delete_applicant_route(request, applicant_id):
    return delete_applicant(applicant_id)
