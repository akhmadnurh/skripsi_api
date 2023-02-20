from sanic import Sanic
from bson.json_util import dumps
from sanic_ext import Extend

app = Sanic("Job_Jobseeker_Score", dumps=dumps)
app.config.CORS_ORIGINS = "*"
Extend(app)

from src.routes import main_route
