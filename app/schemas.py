from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    rating: float = 5.0


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    rating: float

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    year: int | None = None
    rating: float | None = None


class BookResponse(BaseModel):
    success: bool
    data: BookRead
    message: str | None = None
