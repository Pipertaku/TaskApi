from fastapi import FastAPI
from .routers import task, users,login,admin
from fastapi.middleware.cors import CORSMiddleware


origins = ["http://localhost:3000"]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.route)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(task.route)


