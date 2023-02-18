from sanic import Sanic
from bson.json_util import dumps

app = Sanic("Job_Jobseeker_Score", dumps=dumps)

from src.routes import main_route
