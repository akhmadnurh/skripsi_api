from numpy import dot
from numpy.linalg import norm


def cosine_similarity(data):
    result = []
    for index, value in enumerate(data):
        cosim = calc(data[0]["result"], value["result"])
        result.append(cosim)

    return result


def calc(A, B):
    return dot(A, B) / (norm(A) * norm(B))
