from sqlalchemy.orm import Session
from sqlalchemy import Engine
import typing
import time
import structlog

from cheminfra.db.base import Base

TypeTaskCallable = typing.Callable[[Session], None]

class Scheduler:
  def __init__(self):
    self.tasks: typing.Dict[str, TypeTaskCallable] = {}
    self.engine: Engine | None = None
    self.logger = structlog.get_logger()

  def add_task(self, name: str):
    def decorator(func):
      self.tasks[name] = func
      return func
    return decorator
  
  def __loop(self):
    self.logger.info("looping over tasks")
    for task in self.tasks.values():
      with Session(self.engine) as session:
        task(session)

  def run(self, engine: Engine):
    self.engine = engine
    Base.metadata.create_all(engine)
    while True:
      self.__loop()
      time.sleep(5)

scheduler = Scheduler()