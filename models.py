from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

Base=declarative_base()


class Notes(Base):
    __tablename__="notes"
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column()
    content:Mapped[str | None]=mapped_column(default=None)
    user_id:Mapped[str]=mapped_column(ForeignKey("owners.owner_id"))
    date_created:Mapped[datetime]=mapped_column(default=datetime.now())


class User(Base):
    __tablename__="owners"
    owner_id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column()
    hashed_pwd:Mapped[str]=mapped_column()

