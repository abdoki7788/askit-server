from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from forum.routes import routes as forum_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8070",
    "http://127.0.0.1:8070",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forum_routes)

@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse("/static/favicon.png")