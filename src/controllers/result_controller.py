from src.models.database import db
from bson.objectid import ObjectId
from sanic.response import json
from operator import itemgetter

from src.misc.pre_processing import remove_punc, tokenizing


def get_result(data):
    try:
        job_id, applicant_id = itemgetter("job_id", "applicant_id")(data)

        job_data = db["jobstreet"].find_one({"_id": ObjectId(job_id)})
        applicant_data = db["linkedin"].find_one({"_id": ObjectId(applicant_id)})

        result = {}
        result["remove_punct"] = remove_punc(job_data["description"])
        result["tokenizing"] = tokenizing(result["remove_punct"])
        return json(result, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)
