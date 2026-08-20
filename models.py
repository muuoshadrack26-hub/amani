from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column


Base=declarative_base()


class Notes(Base):
    __tablename__="notes"
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column()
    content:Mapped[str | None]=mapped_column(default=None)
    user_id:Mapped[str]=mapped_column(ForeignKey("user_id"))


class User(Base):
    __tablename__="owners"
    owner_id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column()
    hashed_pwd:Mapped[str]=mapped_column()

