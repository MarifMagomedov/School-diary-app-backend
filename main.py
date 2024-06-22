import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api import *
from api.auth import get_current_user


PROTECTED = Depends(get_current_user)

app = FastAPI(
    openapi_url='/openapi.json'
)


app.include_router(auth_router)
app.include_router(teacher_router, dependencies=[PROTECTED])
app.include_router(subject_router, dependencies=[PROTECTED])
app.include_router(classes_router, dependencies=[PROTECTED])
app.include_router(student_router, dependencies=[PROTECTED])
app.include_router(manager_router, dependencies=[PROTECTED])


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


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
