from src.models.database import db
from bson.objectid import ObjectId
from sanic.response import json
from operator import itemgetter
from src.misc.uuid import generate_uuid

from src.misc.pre_processing import (
    remove_punc,
    tokenizing,
    remove_stopword,
    snow_stemming,
)

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


def pre_processing(data):
    try:
        job_id, applicant_id, role = itemgetter("job_id", "applicant_id", "role")(data)

        # Generate UUID
        UUID = generate_uuid()

        result = {}

        job_data = db["jobstreet"].find_one({"_id": ObjectId(job_id)})
        applicants_data = db["linkedin"].find({"role": role})

        # Job Preprocessing
        job_result = {}
        job_result["remove_punct"] = remove_punc(job_data["description"])
        job_result["tokenizing"] = tokenizing(job_result["remove_punct"])
        job_result["no_stopword"] = remove_stopword(job_result["tokenizing"])
        job_result["stem"] = snow_stemming(job_result["no_stopword"])
        job_result["uuid"] = UUID

        # Upload to db
        # db['pre_jobstreet'].insert_one(_result)

        # Applicants Preprocessing
        applicant_result = []
        for applicant in applicants_data:
            _result = {}

            # Merge data
            _headline = applicant["headline"]
            _about = applicant["about"]

            _education = [item.values() for item in applicant["educations"]]
            _education = " ".join([i for education in _education for i in education])

            _experience = [item.values() for item in applicant["experiences"]]
            _experience = " ".join(
                [i for experience in _experience for i in experience]
            )

            _skill = " ".join([skill for skill in applicant["skills"]])

            _license = [item.values() for item in applicant["licenses"]]
            _license = " ".join([i for license in _license for i in license])

            _project = [item.values() for item in applicant["projects"]]
            _project = " ".join([i for project in _project for i in project])

            merged_data = " ".join(
                [_headline, _about, _education, _experience, _skill, _license, _project]
            )

            _result["remove_punct"] = remove_punc(merged_data)
            _result["tokenizing"] = tokenizing(_result["remove_punct"])
            _result["no_stopword"] = remove_stopword(_result["tokenizing"])
            _result["stem"] = snow_stemming(_result["no_stopword"])

            _result["uuid"] = UUID

            # Upload to db
            # db['pre_linkedin'].insert_one(_result)

            if applicant_id == str(applicant["_id"]):
                applicant_result.append(_result)

        result["job"] = job_result
        result["applicant"] = applicant_result

        return json({"result": result, "uuid": UUID}, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)


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
