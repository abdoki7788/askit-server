from fastapi import APIRouter

routes = APIRouter()

@routes.get('/')
def home():
    return {'message': 'Hello World'}