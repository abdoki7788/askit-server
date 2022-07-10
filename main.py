from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from forum.routes import routes as forum_routes
from auth.routes import routes as auth_routes
from tags.routes import routes as tags_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from db_config import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

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
app.include_router(auth_routes)
app.include_router(tags_routes)

@app.get("/favicon.ico")
def favicon():
    return RedirectResponse("/static/favicon.png")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8070)