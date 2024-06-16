import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import *
from utils.middlewares import CurrentUserMiddleware

app = FastAPI(
    openapi_url='/openapi.json'
)


app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(classes_router)
app.include_router(student_router)
app.include_router(manager_router)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CurrentUserMiddleware)


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
