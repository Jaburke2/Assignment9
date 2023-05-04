import abc
from sqlalchemy.orm import Session
from Domain.model import Bookmark
from repository import AbstractRepository

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, bookmark: Bookmark):
        self.db_session.add(bookmark)
        self.db_session.commit()

    def read(self, id: int) -> Bookmark:
        return self.db_session.query(Bookmark).filter_by(id=id).first()

    def read_all(self) -> list[Bookmark]:
        return self.db_session.query(Bookmark).all()

    def update(self, bookmark: Bookmark):
        self.db_session.commit()

    def delete(self, id: int):
        bookmark = self.read(id)
        self.db_session.delete(bookmark)
        self.db_session.commit()
