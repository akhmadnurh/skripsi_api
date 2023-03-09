from main import app
from src.controllers.result_controller import (
    get_result,
    pre_processing,
    get_data_source,
    calc_tf_idf,
    calc_cosine_similarity,
)

BASE_PATH = "/api/result"


@app.get(f"{BASE_PATH}/source")
async def get_data_source_route(request):
    return get_data_source(request.args)


@app.post(f"{BASE_PATH}/")
async def get_result_route(request):
    return get_result(request.json)


@app.post(f"{BASE_PATH}/preprocessing")
async def pre_processing_route(request):
    return pre_processing(request.json)


@app.post(f"{BASE_PATH}/tf-idf")
async def tf_idf_route(request):
    return calc_tf_idf(request.json)


@app.post(f"{BASE_PATH}/cosine-similarity")
async def cosine_similarity_route(request):
    return calc_cosine_similarity(request.json)
