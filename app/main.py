from fastapi import FastAPI

from .db import engine, Base
from . import models
from .routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Management API")

app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Book Management API"}
