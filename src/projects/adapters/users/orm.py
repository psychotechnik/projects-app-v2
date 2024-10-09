from sqlalchemy import (
    Table,
    Column, 
    Integer, 
    String, 
    DateTime,
    Boolean, 
    MetaData,
)
from sqlalchemy.orm import registry

from projects.domain import user

metadata = MetaData()
mapper_registry = registry()

tb_user = Table(
    "users",
    mapper_registry.metadata,
    #metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(64), index=True, unique=True),
    Column("email", String(120), index=True, unique=True),
    Column("is_manager", Boolean),
    Column("password_hash", String(256)),
    Column("token", String(32), index=True, unique=True),
    Column("token_expiration", DateTime),
)

def start_mappers():
    mapper_registry.map_imperatively(user.User, tb_user)

    #user_mapper = mapper(
    #        user.User,
    #        tb_user,
            #properties={
            #    "company": relationship(
            #        domain.Company,
            #        backref="users"
            #     ),
            #},
    #    )
