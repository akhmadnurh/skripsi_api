from main import app
from src.controllers.source_controller import get_data_source
from src.controllers.result_controller import get_result

BASE_PATH = "/api/result"


@app.get(f"{BASE_PATH}/source")
async def get_data_source_route(request):
    return get_data_source(request.args)


@app.post(f"{BASE_PATH}/")
async def get_result_route(request):
    return get_result(request.json)
