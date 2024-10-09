from typing import Optional
from dataclasses import dataclass

from projects.domain.user import User

class Command:
    pass


@dataclass
class CreateUser(Command):
    username: str
    email: str
    password: Optional[str]


@dataclass
class PromoteToManager(Command):
    username: str


@dataclass
class CreateToken(Command):
    username: str

@dataclass
class RevokeToken(Command):
    user: User
