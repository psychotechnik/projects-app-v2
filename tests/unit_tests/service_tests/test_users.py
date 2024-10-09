#import pytest

from projects.domain.user import User
from projects.service_layer.users import handlers
from projects.adapters.users.repository import AbstractRepository as UsersAbstractRepository


class FakeSession:
    committed = False

    def commit(self):
        print("FakeSession.commit called --")
        self.committed = True



class FakeFlaskSQLAlchemy:

    def __init__(self, session: FakeSession):
        super().__init__()
        self.session = session



class FakeUsersRepository(UsersAbstractRepository):

    def __init__(self, users, 
                 #db: FakeFlaskSQLAlchemy
                 ):
        super().__init__()
        self._users = set(users)
        #self.db = db

    @staticmethod
    def for_user(id, username, email):
        user = User(username=username, email=email)
        user.id = id
        return FakeUsersRepository([user])

    def create(self, user):
        self._users.add(user)

    def get(self, id):
        return next(u for u in self._users if u.id == id)

    def list(self):
        return list(self._users)

    def delete(self, user: User) -> None: 
        self._users.remove(user)

    def get_by_email(self, email:str) -> User:
        return next(u for u in self._users if u.email == email)

    def get_by_token(self, token: str) -> User:
        return next(u for u in self._users if u.token == token)

    def get_by_username(self, username: str) -> User:
        return next(u for u in self._users if u.username == username)

    def update(self, user: User) -> User:
        return user
        



#def test_returns_user():
#    repo = FakeUsersRepository.for_user(1, 'test-user-01', 'test-user-01@example.com')
#    user  = handlers.get_user(1, repo)
#    assert user.id == 1

#def test_commits():
#    u1 = User(username='test-user-01', email='test-user-01@example.com')
#    u1.id = 1
#    db = FakeFlaskSQLAlchemy(session=FakeSession())
#    repo = FakeUsersRepository([u1], db)
#    _  = handlers.update_user(u1, repo)

#    assert repo.db.session.committed
