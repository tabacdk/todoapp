from sqlalchemy.orm import declarative_base
from .todo import Todo
from .user import User

__all__ = ["Base", "Todo", "User"]

# This module initializes the SQLAlchemy Base and imports the models.
Base = declarative_base()
