import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.teachers import router as teacher_router
from api.subject import router as subject_router
from api.teachers import router as admin_router
from api.cls import router as classes_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(classes_router)


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
