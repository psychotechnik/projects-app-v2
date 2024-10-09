from typing import List
import abc

from sqlalchemy import select

from projects.domain.user import User


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def create(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_token(self, token: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[User]:
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)

    def update(self, user: User) -> User:
        self.session.add(user)
        return user

    def get(self, id: int) -> User:
        return self.session.query(User).filter_by(id=id).scalar()

    def get_roles(self, token: str) -> str | None:
        user = self.session.query(User).filter_by(token=token).scalar()
        return "manager" if user.is_manager else None

    def get_by_username(self, username: str) -> User:
        return self.session.execute(
                select(User).filter_by(username=username)
        ).scalar()

    def get_by_email(self, email: str) -> User:
        return self.session.execute(
                select(User).filter_by(email=email)
        ).scalar()

    def get_by_token(self, token: str) -> User:
        return self.session.execute(
                select(User).filter_by(token=token)
        ).scalar()

    def delete(self, user: User) -> None:
        self.session.delete(user)

    def list(self) -> List[User]:
        return self.session.execute(
                select(User).order_by(User.username)
        ).scalars()
