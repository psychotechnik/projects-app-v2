from typing import List
import abc
from sqlalchemy.orm import joinedload

from projects.domain.project import Project
from projects.domain.task import Task


class AbstractRepository(abc.ABC):
    
    # Project
    @abc.abstractmethod
    def create_project(self, project: Project):
        raise NotImplementedError

    @abc.abstractmethod
    def update_project(self, project: Project):
        raise NotImplementedError

    @abc.abstractmethod
    def get_project(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_project(self, project: Project):
        raise NotImplementedError

    @abc.abstractmethod
    def list_projects(self) -> List[Project]:
        raise NotImplementedError
    
    #Task
    @abc.abstractmethod
    def create_task(self, task: Task):
        raise NotImplementedError

    @abc.abstractmethod
    def update_task(self, task: Task):
        raise NotImplementedError

    @abc.abstractmethod
    def get_task(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_task(self, task: Task):
        raise NotImplementedError

    @abc.abstractmethod
    def list_tasks(self) -> List[Task]:
        raise NotImplementedError


class SqlAlchemyProjectRepository(AbstractRepository):
    
    # Project
    def __init__(self, session):
        self.session = session

    def create_project(self, project: Project):
        self.session.add(project)

    def update_project(self, project: Project) -> Project:
        self.session.add(project)
        return project

    def get_project(self, id: int) -> Project:     
        return self.session.query(Project).options(
                joinedload(Project.tasks)
        ).filter_by(id=id).one_or_none()
        
    def delete_project(self, project: Project) -> None:
        self.session.delete(project)

    # Load all projects with related tasks using joinedload
    def list_projects(self) -> List[Project]:        
        return self.session.query(Project).options(joinedload(Project.tasks)).all()

    #Task
    
    def create_task(self, task: Task):
        self.session.add(task)

    def update_task(self, task: Task) -> Task:
        self.session.add(task)
        return task

    def get_task(self, id: int) -> Task:
        return self.session.query(Task).filter_by(id=id).scalar()

    def delete_task(self, task: Task) -> None:
        self.session.delete(task)
           
    def list_tasks(self, project_id: int) -> List[Task]:
        return self.session.query(Task).filter_by(project_id=project_id).order_by(Task.id).all()

