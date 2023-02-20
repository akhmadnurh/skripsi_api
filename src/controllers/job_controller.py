from src.models.database import db
from bson.objectid import ObjectId
from sanic.response import json
from operator import itemgetter


def get_jobs():
    try:
        res = db["jobstreet"].find().sort("_id", -1)

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"message": "Job was not found"}, status=404)
    except Exception as e:
        return json({"message": str(e)}, status=500)


def get_jobs_brief():
    try:
        res = (
            db["jobstreet"]
            .find({}, {"_id": 1, "job_name": 1, "description": 1, "company": 1})
            .sort("_id", -1)
        )

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"message": "Job was not found"}, status=404)

    except Exception as e:
        return json({"message": str(e)}, status=500)


def get_job_by_id(job_id):
    try:
        res = db["jobstreet"].find_one({"_id": ObjectId(job_id)})

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"message": "Job was not found."}, status=404)
    except Exception as e:
        return json({"message": str(e)}, status=500)


def create_job(data={}):
    try:
        url, role, job_name, company, location, description = itemgetter(
            "url", "role", "job_name", "company", "location", "description"
        )(data)

        try:
            res = db["jobstreet"].insert_one(
                {
                    "url": url,
                    "role": role,
                    "job_name": job_name,
                    "company": company,
                    "location": location,
                    "description": description,
                }
            )
            return json({"message": "Job was added successfully."}, status=200)
        except Exception as e:
            return json({"message": str(e)}, status=500)

    except Exception as e:
        print(e)
        return json({"message": "Please insert the required fields."}, status=400)


def update_job(job_id, data={}):
    try:
        url, role, job_name, company, location, description = itemgetter(
            "url", "role", "job_name", "company", "location", "description"
        )(data)

        try:
            res = db["jobstreet"].update_one(
                {"_id": ObjectId(job_id)},
                {
                    "$set": {
                        "url": url,
                        "role": role,
                        "job_name": job_name,
                        "company": company,
                        "location": location,
                        "description": description,
                    }
                },
            )
            return json({"message": "Job was updated successfully."}, status=200)
        except Exception as e:
            return json({"message": str(e)}, status=500)

    except Exception as e:
        print(e)
        return json({"message": "Please insert the required fields."}, status=400)


def delete_job(job_id):
    try:
        res = db["jobstreet"].delete_one({"_id": ObjectId(job_id)})

        return json({"message": "Job was deleted successfully."}, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)
