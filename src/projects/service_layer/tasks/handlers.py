from typing import List

from projects.service_layer.projects import unit_of_work
from projects.domain.task import Task


def create_task(project_id: int, name: str, status:str, uow: unit_of_work.AbstractUnitOfWork) -> Task:
    """Creates a new task in the project."""
    with uow:
        task = Task(project_id=project_id, name=name, status=status)
        uow.repo.create_task(task)
        uow.session.commit()
        return task.to_dict()

def get_task(id: int, uow: unit_of_work.AbstractUnitOfWork) -> Task:
    """Gets a task by its ID."""
    with uow:    
        return uow.repo.get_task(id)

def get_tasks_for_project(project_id: int, uow: unit_of_work.AbstractUnitOfWork) -> List[Task]:
    """Gets all tasks for a specific project."""
    with uow:
        data = []
        for task in uow.repo.list_tasks(project_id):
            data.append(task.to_dict())
        return data

def update_task_status(project_id: int, task_id: int, status: str, uow: unit_of_work.AbstractUnitOfWork) -> Task:
    """Updates the task status."""
    with uow:
        task = uow.repo.get_task(task_id)
        if task.project_id == project_id:
            task.status = status  
            uow.repo.update_task(task)
            uow.session.commit()        
            return task.to_dict()
        return None

def delete_task(id: int, uow: unit_of_work.AbstractUnitOfWork):
    """Deletes a task by its ID."""
    with uow:
        task = uow.repo.get_task(id)
        if task:
            uow.repo.delete_task(task)
            uow.session.commit() 
