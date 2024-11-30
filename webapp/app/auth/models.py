from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base, str_uniq

from app.game.models import Game, game_user_association

class Role(Base):
    name: Mapped[str_uniq]
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class User(Base):
    name: Mapped[str_uniq]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, server_default=text("1"))

    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")
    games: Mapped[list[Game]] = relationship(secondary=game_user_association, back_populates="users")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"