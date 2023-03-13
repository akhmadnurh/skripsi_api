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

from src.misc.tf_idf import tf_idf
from src.misc.cosine_similarity import cosine_similarity


def get_result(data):
    try:
        uuid = itemgetter("uuid")(data)

        result = list(
            db["cosine_similarity"].aggregate(
                [
                    {"$match": {"uuid": uuid, "type": "applicant"}},
                    {
                        "$lookup": {
                            "from": "linkedin",
                            "localField": "ref_id",
                            "foreignField": "_id",
                            "as": "applicant",
                            "pipeline": [
                                {
                                    "$project": {
                                        "_id": 1,
                                        "url": 1,
                                        "role": 1,
                                        "fullname": 1,
                                    }
                                }
                            ],
                        },
                    },
                    {"$project": {"_id": 1, "result": 1, "applicant": 1, "ref_id": 1}},
                    {"$sort": {"result": -1}},
                ]
            )
        )
        return json(result, status=200)
    except Exception as e:
        return json({"message": str(e)}, status=500)


def pre_processing(data):
    try:
        job_id, applicant_id, role = itemgetter("job_id", "applicant_id", "role")(data)

        # Generate UUID
        UUID = generate_uuid()

        result = {}

        # Data source
        job_data = db["jobstreet"].find_one({"_id": ObjectId(job_id)})
        applicants_data = list(db["linkedin"].find({"role": role}))

        # Job Preprocessing
        job_result = {}
        job_result["remove_punct"] = remove_punc(job_data["description"])
        job_result["tokenizing"] = tokenizing(job_result["remove_punct"])
        job_result["no_stopword"] = remove_stopword(job_result["tokenizing"])
        job_result["stem"] = snow_stemming(job_result["no_stopword"])

        # Upload job preprocessing to db
        job_result = {
            "uuid": UUID,
            "type": "job",
            "ref_id": job_data["_id"],
            "result": job_result,
        }
        db["text_preprocessing"].insert_one(job_result)

        # Applicants Preprocessing
        applicant_results = []
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

            _remove_punct = remove_punc(merged_data)
            _tokenizing = tokenizing(_remove_punct)
            _no_stopword = remove_stopword(_tokenizing)
            _stem = snow_stemming(_no_stopword)

            _result["result"] = {
                "remove_punct": _remove_punct,
                "tokenizing": _tokenizing,
                "no_stopword": _no_stopword,
                "stem": _stem,
            }

            _result["type"] = "applicant"
            _result["uuid"] = UUID
            _result["ref_id"] = applicant["_id"]

            applicant_results.append(_result)

        # Upload to applicant preprocessing
        db["text_preprocessing"].insert_many(applicant_results)

        # Response data
        result["job"] = db["text_preprocessing"].find_one(
            {"type": "job", "uuid": UUID, "ref_id": ObjectId(job_id)}
        )
        result["applicant"] = db["text_preprocessing"].find_one(
            {
                "type": "applicant",
                "uuid": UUID,
                "ref_id": ObjectId(applicant_id),
            }
        )
        result["uuid"] = UUID

        return json({"result": result}, status=200)
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


def calc_tf_idf(data):
    try:
        job_id, applicant_id, uuid = itemgetter("job_id", "applicant_id", "uuid")(data)
        pre_data = list(db["text_preprocessing"].find({"uuid": uuid}))
        result = tf_idf(pre_data)

        # Upload data
        feature_names, tf_idf_results = result

        for index in range(len(tf_idf_results)):
            tf_idf_results[index] = {
                "feature_names": feature_names,
                "ref_id": pre_data[index]["ref_id"],
                "result": tf_idf_results[index],
                "type": "applicant",
                "uuid": uuid,
            }
            if pre_data[index]["type"] == "job":
                tf_idf_results[index]["type"] = "job"

        db["term_weighting"].insert_many(tf_idf_results)

        # Response data
        response = {}
        response["job"] = db["term_weighting"].find_one(
            {"type": "job", "uuid": uuid, "ref_id": ObjectId(job_id)}
        )
        response["applicant"] = db["term_weighting"].find_one(
            {
                "type": "applicant",
                "uuid": uuid,
                "ref_id": ObjectId(applicant_id),
            }
        )
        response["uuid"] = uuid

        return json(
            {"result": response},
            status=200,
        )
    except Exception as e:
        return json({"message": str(e)}, status=500)


def calc_cosine_similarity(data):
    try:
        job_id, applicant_id, uuid = itemgetter("job_id", "applicant_id", "uuid")(data)

        tf_idf = list(db["term_weighting"].find({"uuid": uuid}))

        result = cosine_similarity(tf_idf)
        for index in range(len(result)):
            result[index] = {
                "ref_id": tf_idf[index]["ref_id"],
                "result": result[index],
                "uuid": uuid,
                "type": (
                    "job"
                    if tf_idf[index]["ref_id"] == ObjectId(job_id)
                    else "applicant"
                ),
            }

        # Upload to db
        db["cosine_similarity"].insert_many(result)

        # Response data
        response = {}
        response["job"] = db["cosine_similarity"].find_one(
            {"uuid": uuid, "ref_id": ObjectId(job_id)}
        )
        response["applicant"] = db["cosine_similarity"].find_one(
            {
                "uuid": uuid,
                "ref_id": ObjectId(applicant_id),
            }
        )
        response["uuid"] = uuid

        return json(
            {"result": response},
            status=200,
        )
    except Exception as e:
        return json({"message": str(e)}, status=500)
