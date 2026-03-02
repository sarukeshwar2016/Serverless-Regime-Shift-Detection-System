"""
AWS Lambda handler for the REST API.
Uses Mangum to wrap the FastAPI app for API Gateway / Lambda.
"""

from mangum import Mangum
from api.main import app

handler = Mangum(app, lifespan="off")
