from cheminfra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime


class Container(Base):
  __tablename__ = "containers"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  display_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  container_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  statuses: Mapped[list["ContainerStatus"]] = relationship(back_populates="container")


class ContainerStatus(Base):
  __tablename__ = "container_status"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)

  container_id: Mapped[int] = mapped_column(Integer, ForeignKey("containers.id"), nullable=False)
  container: Mapped["Container"] = relationship(back_populates="statuses")

  status: Mapped[str] = mapped_column(String, nullable=False)
  recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
