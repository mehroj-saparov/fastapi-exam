from sqlalchemy.orm import Session
from app.db import get_db, engine
from app.models import Book

books_data = [
    {"title": "Harry Potter", "author": "J.K. Rowling", "genre": "Fantasy", "year": 1997, "rating": 4.9},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937, "rating": 4.8},
    {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "year": 1949, "rating": 4.7},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "year": 1960, "rating": 4.9},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "year": 1951, "rating": 4.2},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "year": 1813, "rating": 4.6},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": 1925, "rating": 4.5},
    {"title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure", "year": 1851, "rating": 4.0},
    {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical", "year": 1869, "rating": 4.4},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Fiction", "year": 1988, "rating": 4.3},
]

db: Session = Session(bind=engine)

for book in books_data:
    new_book = Book(**book)
    db.add(new_book)

db.commit()
db.close()

print("10 ta kitob muvaffaqiyatli kiritildi!")
