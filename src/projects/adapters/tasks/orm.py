from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import registry
from projects.domain import task

mapper_registry = registry()

tasks = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id"), nullable=False),
    Column("name", String(100), nullable=False),
    Column("status", String(100), nullable=True)
)

def start_mappers():
    mapper_registry.map_imperatively(task.Task, tasks)
    