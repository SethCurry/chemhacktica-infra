from cheminfra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime


class BotCommand(Base):
    __tablename__ = "bot_commands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command: Mapped[str] = mapped_column(String, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    user: Mapped[str] = mapped_column(String, nullable=False)
