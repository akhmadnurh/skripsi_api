import os
import pymongo
from dotenv import load_dotenv

# Load env
load_dotenv()

client = pymongo.MongoClient(os.getenv("DATABASE_URL"))

db = client["skripsi"]


def test():
    print("oke")


# print(db["jobstreet"].find_one())
