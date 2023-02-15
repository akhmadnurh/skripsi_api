from main import app
from src.controllers import pre_controller

base_path = "/api/pre"


@app.post(f"{base_path}")
def pre():
    return pre_controller.pre()
