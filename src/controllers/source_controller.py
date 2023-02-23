from sanic.response import json
from bson.objectid import ObjectId
from src.models.database import db
from operator import itemgetter


def get_data_source(args):
    try:
        job_id, applicant_id = itemgetter("job_id", "applicant_id")(args)

        job_id = job_id[0]
        applicant_id = applicant_id[0]

        # Job Data
        job = db["jobstreet"].find_one({"_id": ObjectId(job_id)})

        applicant = db["linkedin"].find_one({"_id": ObjectId(applicant_id)})

        return json({"data": {"job": job, "applicant": applicant}}, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)
