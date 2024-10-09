from sqlalchemy import (
    Table,
    Column, 
    Integer, 
    String, 
    ForeignKey,
)
from sqlalchemy.orm import registry
# from projects.entrypoints.flask import db
from sqlalchemy.orm import registry, relationship
from projects.domain import project, task, user

mapper_registry = registry()
    
tb_projects = Table(
    "projects",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("description", String(255), nullable=True)
)


tb_tasks = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id"), nullable=False),
    Column("name", String(100), nullable=False),
    Column("status", String(100), nullable=True)
)


#members = Table(
#    "members",
#    mapper_registry.metadata,
#    Column("id", Integer, primary_key=True, autoincrement=True),
#    Column("name", String(255)),
#)

#tb_project_members = Table(
#    "members",
#    mapper_registry.metadata,
#    #Column("id", Integer, primary_key=True),
#    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
#    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
#)

  
def start_mappers():

    #members_mapper = mapper_registry.map_imperatively(
    #    user.User, 
    #    project_members,
    #)

    mapper_registry.map_imperatively(
        project.Project,
        tb_projects,
        properties={
            # Enable cascade delete for tasks when a project is deleted
            'tasks': relationship(
                task.Task, 
                backref='project', 
                cascade="all, delete-orphan", 
                lazy='joined'
            ),
            #'_members': relationship(
            #    members_mapper, 
            #    secondary=project_members, 
            #    backref='tb_projects',
            #    collection_class=set,
            #),

        }
    )

    mapper_registry.map_imperatively(task.Task, tb_tasks)
