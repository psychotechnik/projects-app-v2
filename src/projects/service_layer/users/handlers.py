import secrets
from datetime import datetime, timezone, timedelta
from typing import List

from projects.domain.user import User
from projects.domain import commands
from projects.service_layer.users import unit_of_work


def create(
        cmd: commands.CreateUser, 
        uow: unit_of_work.AbstractUnitOfWork,
        ) -> None:

    with uow:
        user = User(username=cmd.username, email=cmd.email)
        if cmd.password:
            user.set_password(cmd.password)
        uow.repo.create(user)
        uow.session.commit()

def verify_password(username, password, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.repo.get_by_username(username)
        if user and user.check_password(password):
            return user

def get_roles(token: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        return uow.repo.get_roles(token)

def get_user(id: int, uow: unit_of_work.AbstractUnitOfWork) -> dict | None:
    with uow:
        user = uow.repo.get(id)
        if user:
            return user.to_dict()

def get_user_by_username(username: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.repo.get_by_username(username)
        if user:
            return user.to_dict()

def get_user_by_email(email: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        return uow.repo.get_by_email(email)

def update_user(user: User, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.repo.update(user)
        uow.session.commit()
        return user

def get_users(uow: unit_of_work.AbstractUnitOfWork) -> List[User]:
    with uow:
        data = []
        for user in uow.repo.list():
            data.append(user.to_dict())
        return data

def create_token(
        cmd: commands.CreateToken, 
        uow: unit_of_work.AbstractUnitOfWork,
        ) -> None:

    with uow:
        now = datetime.now(timezone.utc)
        expires_in = 86400

        user = uow.repo.get_by_username(cmd.username)

        if user.token and user.token_expiration.replace(
                tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return

        token = secrets.token_hex(16)
        token_expiration = now + timedelta(seconds=expires_in)

        user.token = token
        user.token_expiration = token_expiration
        uow.repo.create(user)
        uow.session.commit()

#def issue_new_token(
#        user: User, 
#        expires_in: int, 
#        uow: unit_of_work.AbstractUnitOfWork,
#    ) -> str:
#    now = datetime.now(timezone.utc)
#    token = secrets.token_hex(16)
#    token_expiration = now + timedelta(seconds=expires_in)

#    with uow:
#        user.token = token
#        user.token_expiration = token_expiration
#        uow.repo.create(user)
#        uow.session.commit()

#        return user.token

def revoke_token(cmd: commands.RevokeToken, 
                 uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        cmd.user.revoke_token()
        uow.repo.update(cmd.user)
        uow.session.commit()

def check_token(token, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.repo.get_by_token(token)
        if user is None or user.token_expiration.replace(
                tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user

def promote_to_manager(
        cmd: commands.PromoteToManager, 
        uow: unit_of_work.AbstractUnitOfWork,
        ) -> bool | None:

    with uow:
        user = uow.repo.get_by_username(cmd.username)
        user.is_manager = True
        uow.session.commit()
        return True

def delete_user(id: int, uow: unit_of_work.AbstractUnitOfWork):

    with uow:
        user = uow.repo.get(id)
        uow.repo.delete(user) 
        uow.session.commit() 
