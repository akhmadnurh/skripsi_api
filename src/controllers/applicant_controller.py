from src.models.database import db
from sanic.response import json
from bson.objectid import ObjectId
from operator import itemgetter


def get_applicants():
    try:
        res = db["linkedin"].find().sort("_id", -1)

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"message": "Applicant was not found."}, status=404)
    except Exception as e:
        return json({"message": str(e)}, status=500)


def get_applicants_brief(data={}):
    try:
        # Get job role
        job_id = data["job_id"][0]
        # job_id = job_id
        print(job_id)
        # Get job
        job = db["jobstreet"].find_one({"_id": ObjectId(job_id)})
        if job:
            res = (
                db["linkedin"]
                .find({"role": job["role"]}, {"_id": 1, "fullname": 1, "headline": 1})
                .sort("_id", -1)
            )

            if res:
                return json({"data": res}, status=200)
            else:
                return json({"message": "Applicant was not found."}, status=404)
        else:
            return json({"message": "Applicant was not found."}, status=404)

    except Exception as e:
        return json({"message": str(e)}, status=500)


def get_applicant_by_id(applicant_id):
    try:
        res = db["linkedin"].find_one({"_id": ObjectId(applicant_id)})

        if res:
            return json({"data": res}, status=200)
        else:
            return json({"message": "Applicant was not found."}, status=404)
    except Exception as e:
        return json({"message": str(e)}, status=500)


def create_applicant(data={}):
    try:
        (
            url,
            role,
            fullname,
            headline,
            about,
            educations,
            experiences,
            skills,
            licences,
            projects,
        ) = itemgetter(
            "url",
            "role",
            "fullname",
            "headline",
            "about",
            "educations",
            "experiences",
            "skills",
            "licences",
            "projects",
        )(
            data
        )

        try:
            res = db["linkedin"].insert_one(
                {
                    "url": url,
                    "role": role,
                    "fullname": fullname,
                    "headline": headline,
                    "about": about,
                    "educations": educations,
                    "experiences": experiences,
                    "skills": skills,
                    "licences": licences,
                    "projects": projects,
                }
            )
            return json({"message": "Applicant was added successfully."}, status=200)
        except Exception as e:
            return json({"message": str(e)}, status=500)
    except Exception as e:
        return json({"message": "Please insert the required fields."}, status=400)


def update_applicant(applicant_id, data={}):
    try:
        (
            url,
            role,
            fullname,
            headline,
            about,
            educations,
            experiences,
            skills,
            licences,
            projects,
        ) = itemgetter(
            "url",
            "role",
            "fullname",
            "headline",
            "about",
            "educations",
            "experiences",
            "skills",
            "licences",
            "projects",
        )(
            data
        )

        try:
            res = db["linkedin"].update_one(
                {"_id": ObjectId(applicant_id)},
                {
                    "$set": {
                        "url": url,
                        "role": role,
                        "fullname": fullname,
                        "headline": headline,
                        "about": about,
                        "educations": educations,
                        "experiences": experiences,
                        "skills": skills,
                        "licences": licences,
                        "projects": projects,
                    }
                },
            )
            return json(
                {"message": "Applicant was updated successfully."},
                status=200,
            )
        except Exception as e:
            print(e)
            return json({"message": str(e)}, status=500)
    except Exception as e:
        return json({"message": "Please insert the required fields."}, status=400)


def delete_applicant(applicant_id):
    try:
        res = db["linkedin"].delete_one({"_id": ObjectId(applicant_id)})

        return json({"message": "Applicant was deleted successfully."}, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)
