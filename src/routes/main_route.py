from sanic import json
from main import app

# Import all routes
from src.routes import job_route
from src.routes import applicant_route
from src.routes import result_route


@app.get("/")
async def main(request):
    return json({"msg": "Welcome to Server"})
