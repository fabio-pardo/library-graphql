from __future__ import annotations

import strawberry
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from strawberry.fastapi import GraphQLRouter

from db.models import Author, Book

# --- Database setup ---
DATABASE_URL = "postgresql+psycopg2://user:password@localhost/library"
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine))


# --- GraphQL types ---
@strawberry.type
class BookType:
    id: int
    title: str
    genre: str
    published_year: int
    author: AuthorType


@strawberry.type
class AuthorType:
    id: int
    name: str
    nationality: str
    books: list[BookType]


@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    reading_list: list[BookType]


def to_author_type(author: Author, include_books: bool = False) -> AuthorType:
    return AuthorType(
        id=author.id,
        name=author.name,
        nationality=author.nationality,
        books=(
            [to_book_type(book, include_author=False) for book in author.books]
            if include_books
            else []
        ),
    )


def to_book_type(book: Book, include_author: bool = True) -> BookType:
    author: AuthorType = (
        to_author_type(book.author)
        if include_author
        else AuthorType(id=0, name="", nationality="", books=[])
    )
    return BookType(
        id=book.id,
        title=book.title,
        genre=book.genre,
        published_year=book.published_year,
        author=author,
    )


# --- Query ---
@strawberry.type
class Query:
    @strawberry.field
    def all_books(self) -> list[BookType]:
        db = SessionLocal()
        books: list[Book] = db.query(Book).all()
        result: list[BookType] = [
            BookType(
                id=b.id,
                title=b.title,
                genre=b.genre,
                published_year=b.published_year,
                author=AuthorType(
                    id=b.author.id,
                    name=b.author.name,
                    nationality=b.author.nationality,
                    books=[to_book_type(ab) for ab in b.author.books],
                ),
            )
            for b in books
        ]
        db.close()
        return result


# --- FastAPI App ---
schema = strawberry.Schema(query=Query)
gql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(gql_app, prefix="/graphql")
