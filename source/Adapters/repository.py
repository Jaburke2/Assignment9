import abc
from sqlalchemy.orm import Session
from Domain.model import Bookmark

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, bookmark: Bookmark):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, id: int) -> Bookmark:
        raise NotImplementedError

    @abc.abstractmethod
    def read_all(self) -> list[Bookmark]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, bookmark: Bookmark):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int):
        raise NotImplementedError


