from fastapi import Depends, FastAPI
from .routers import todo, user, auth
from app import oauth2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "Todo API"
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router)
app.include_router(user.router) 
app.include_router(oauth2.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"hello": "world"}

