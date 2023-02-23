from main import app
from src.controllers.source_controller import get_data_source

BASE_PATH = "/api/result"


@app.get(f"{BASE_PATH}/source")
async def get_data_source_route(request):
    return get_data_source(request.args)
