from main import app
from src.controllers.applicant_controller import get_applicants, get_applicant_by_id

BASE_PATH = "/api/applicant"


@app.get(f"{BASE_PATH}")
def get_applicant_route(request):
    return get_applicants()


@app.get(f"{BASE_PATH}/<applicant_id>")
def get_applicant_by_id_route(request, applicant_id):
    return get_applicant_by_id(applicant_id)
