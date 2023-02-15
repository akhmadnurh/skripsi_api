from src.misc import pre_processing


def pre():
    # req = request.get_json()
    # data = req["data"]
    data = "ok"
    return pre_processing.remove_punc(data)
