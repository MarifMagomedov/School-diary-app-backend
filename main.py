import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    auth_router,
    teacher_router,
    student_router,
    subject_router,
    classes_router
)


app = FastAPI(
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json',  # This line solved my issue, in my case it was a lambda function
    redoc_url=None
)


app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(classes_router)
app.include_router(student_router)


origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
