from datetime import datetime
from sqlalchemy import text, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base, str_uniq

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.auth.models import User
else:
    User = "User"


game_user_association = Table(
    "game_user_association",
    Base.metadata,
    Column("game_id", ForeignKey("games.id")),
    Column("user_id", ForeignKey("users.id"))
)


class Game(Base):
    name: Mapped[str_uniq]
    password: Mapped[str]
    started_at: Mapped[datetime | None] = None
    ended_at: Mapped[datetime | None] = None
    host_id: Mapped[int] = mapped_column(ForeignKey('users.id'), default=1, server_default=text("1"))

    host: Mapped[User] = relationship("User")
    users: Mapped[User] = relationship("User", secondary=game_user_association, back_populates="games")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, password={self.password}"
