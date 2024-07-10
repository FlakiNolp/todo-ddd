import datetime
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TIMESTAMP


class Base(DeclarativeBase):
    __table_args__ = {"schema": "public"}
    oid: Mapped[uuid.UUID] = mapped_column(primary_key=True, comment="uuid элемента")


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False, unique=False)
    tasks: Mapped["Task"] = relationship(
        "Task", lazy="selectin", back_populates="user", cascade="all, delete"
    )
    categories: Mapped["Category"] = relationship(
        "Category", lazy="selectin", back_populates="user", cascade="all, delete"
    )


class Category(Base):
    __tablename__ = "category"
    user_oid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(User.oid, ondelete="cascade", onupdate="cascade"), nullable=False
    )
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    user: Mapped[User] = relationship(
        "User", back_populates="categories", lazy="selectin"
    )
    tasks: Mapped["Task"] = relationship(
        "Task", back_populates="category", cascade="all, delete", lazy="selectin"
    )


class Task(Base):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(nullable=False)
    is_complete: Mapped[bool] = mapped_column(default=False, nullable=False)
    deadline: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True
    )
    user_oid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(User.oid, ondelete="cascade", onupdate="cascade"), nullable=False
    )
    category_oid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Category.oid, ondelete="cascade", onupdate="cascade"),
        nullable=True,
        default=None,
    )
    user: Mapped[User] = relationship("User", back_populates="tasks", lazy="selectin")
    category: Mapped[Category] = relationship(
        "Category", back_populates="tasks", lazy="selectin"
    )
