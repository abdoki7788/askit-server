from fastapi import FastAPI
from forum.routes import routes as forum_routes

app = FastAPI()

app.include_router(forum_routes)