from typing import List

from . import unit_of_work
from projects.domain.project import Project


def create_project(name: str, description: str, uow: unit_of_work.AbstractUnitOfWork) -> Project:
    """Creates a new project."""
    with uow:
        project = Project(name=name, description=description)
        uow.repo.create_project(project)
        uow.session.commit()
        return project.to_dict()
        
def get_project(id: int, uow: unit_of_work.AbstractUnitOfWork) -> Project:
    """Gets a project by its ID."""
    with uow:
        project = uow.repo.get_project(id)
        if project:
            return project.to_dict()

def list_projects(uow: unit_of_work.AbstractUnitOfWork) -> List[Project]:
    """Gets a list of all projects."""
    with uow:
        data = []
        for project in uow.repo.list_projects():
            data.append(project.to_dict())
        return data

def update_project(id: int, name: str, description: str, uow: unit_of_work.AbstractUnitOfWork) -> Project:
    """Updates an existing project."""
    with uow:
        project = uow.repo.get_project(id)
        if project:           
            if name is not None:
                project.name = name
            if description is not None:
                project.description=description                
            uow.repo.update_project(project) 
            uow.session.commit()    
            return project.to_dict()

def delete_project(id: int, uow: unit_of_work.AbstractUnitOfWork):
    """Deletes a project by its ID."""
    with uow:
        project = uow.repo.get_project(id) # If Project not found retun None
        if project:
            uow.repo.delete_project(project)
            uow.session.commit()
        return project 

