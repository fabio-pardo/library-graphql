# --- Models ---
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String


class Base(DeclarativeBase):
    pass


reading_list_table = Table(
    "reading_list",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
)


class User(Base):
    __tablename__: str = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    reading_list: Mapped[list["Book"]] = relationship(
        "Book", secondary=reading_list_table, back_populates="readers"
    )


class Author(Base):
    __tablename__: str = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    nationality: Mapped[str] = mapped_column(String)
    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__: str = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    published_year: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    author: Mapped[Author] = relationship("Author", back_populates="books")
    readers: Mapped[list[User]] = relationship(
        "User", secondary=reading_list_table, back_populates="reading_list"
    )
