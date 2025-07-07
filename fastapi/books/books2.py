from dataclasses import field
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    published_date: int
    rating: int

    def __init__(self, id, title, author, description, published_date, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date = published_date
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    published_date: int = Field(gt=1999, lt=2031)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra" : {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "published_date": 2024,
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 2012, 5),
    Book(2, 'Be fast with FastAPI', 'codingwithroby', 'Good', 2010, 4),
    Book(3, 'Master Endpoints', 'codingwithroby', 'Nice', 2022, 3),
    Book(4, 'HP1', 'codingwithroby', 'Perfect', 2023, 4),
    Book(5, 'HP2', 'codingwithroby', 'Not bad', 2024, 3),
    Book(6, 'HP3', 'codingwithroby', 'shit', 2025, 1),
]

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get ("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book", status_code=status.HTTP_200_OK)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
        if not book_change:
            raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/by_date/")
def published_date(published_date: int = Query(gt=1999, lt=2027)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')
        
        

# @app.get("/books/find_by_id")
# async def find_by_id(book_id: BookID):
#     book = [f for f in BOOKS if f.id == book_id.id]
#     return book

