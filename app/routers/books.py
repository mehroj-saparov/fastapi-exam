from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from ..db import get_db
from ..models import Book
from ..schemas import BookCreate, BookRead, BookResponse, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.get("/", response_model=List[BookRead])
def get_all_books(db: Session = Depends(get_db)) -> List[BookRead]:
    books = db.query(Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return [BookRead(**book.__dict__) for book in books]


@router.get("/search", response_model=List[BookRead])
def search_books(search: str = Query(..., min_length=1, description="Search by title or author"),
                 db: Session = Depends(get_db)):
    books = db.query(Book).filter(
        or_(
            Book.title.ilike(f"%{search}%"),
            Book.author.ilike(f"%{search}%")
        )
    ).all()

    if not books:
        raise HTTPException(status_code=404, detail="Books not found")
    return [BookRead(**book.__dict__) for book in books]


@router.get("/filter", response_model=List[BookRead])
def filter_books(
    min: int = Query(..., description="Minimum year"),
    max: int = Query(..., description="Maximum year"),
    db: Session = Depends(get_db)
):
    books = db.query(Book).filter(
        Book.year >= min,
        Book.year <= max
    ).all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found in the given year range")
    return [BookRead(**book.__dict__) for book in books]


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> BookResponse:
    new_book = Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        year=book.year,
        rating=book.rating
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return BookResponse(
        success=True,
        data=BookRead(**new_book.__dict__),
        message="Book successfully created"
    )


@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book_data: BookUpdate, db: Session = Depends(get_db)) -> BookResponse:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_data.title is not None:
        book.title = book_data.title
    if book_data.author is not None:
        book.author = book_data.author
    if book_data.genre is not None:
        book.genre = book_data.genre
    if book_data.year is not None:
        book.year = book_data.year
    if book_data.rating is not None:
        book.rating = book_data.rating

    db.commit()
    db.refresh(book)

    return BookResponse(
        success=True,
        data=BookRead(**book.__dict__),
        message="Book successfully updated"
    )


@router.delete("/{id}", response_model=BookResponse)
def delete_book(id: int, db: Session = Depends(get_db)) -> BookResponse:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = BookRead(**book.__dict__)
    db.delete(book)
    db.commit()

    return BookResponse(
        success=True,
        data=book_data,
        message="Book successfully deleted"
    )


@router.get("/{id}", response_model=BookResponse)
def get_book_by_id(id: int, db: Session = Depends(get_db)) -> BookResponse:
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return BookResponse(
        success=True,
        data=BookRead(**book.__dict__),
        message="Book found"
    )