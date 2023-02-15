from src.models.database import db
from bson.objectid import ObjectId
from sanic.response import json


def get_jobs():
    try:
        res = db["jobstreet"].find().sort("_id", -1)

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"msg": "Data not found"}, status=404)
    except Exception as e:
        return json({"msg": str(e)}, status=500)


def get_job_by_id(job_id):
    try:
        res = db["jobstreet"].find_one({"_id": ObjectId(job_id)})

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"msg": "Not Found"}, status=404)
    except Exception as e:
        return json({"msg": str(e)}, status=500)
