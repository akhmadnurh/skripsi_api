from src.models.database import db
from sanic.response import json
from bson.objectid import ObjectId


def get_applicants():
    try:
        res = db["linkedin"].find().sort("_id", -1)

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"msg": "Data not found."}, status=404)
    except Exception as e:
        return json({"msg": str(e)}, status=500)


def get_applicant_by_id(applicant_id):
    try:
        res = db["linkedin"].find_one({"_id": ObjectId(applicant_id)})

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"msg": "Data not found."}, status=404)
    except Exception as e:
        return json({"msg": str(e)}, status=500)
