from projects.adapters.projects.repository import AbstractRepository
from typing import List

from projects.domain.project import Project
from projects.domain.task import Task

# fake_repository.py
class FakeRepository(AbstractRepository):
    def __init__(self, projects: List[Project] = None, tasks: List[Task] = None):
        self._projects = projects or []
        self._tasks = tasks or []
    
    # Project
    def create_project(self, project: Project):
        self._projects.append(project)
    
    def update_project(self, project: Project) -> Project:
        for idx, p in enumerate(self._projects):
            if p.id == project.id:
                self._projects[idx] = project
                return project
    
    def get_project(self, id: int) -> Project:
        return next((p for p in self._projects if p.id == id), None)
    
    def delete_project(self, project: Project):
        self._projects = [p for p in self._projects if p.id != project.id]
    
    def list_projects(self) -> List[Project]:
        return self._projects

    # Task
    def create_task(self, task: Task):
        self._tasks.append(task)
    
    def update_task(self, task: Task) -> Task:
        for idx, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[idx] = task
                return task
    
    def get_task(self, id: int) -> Task:
        return next((t for t in self._tasks if t.id == id), None)
    
    def delete_task(self, task: Task):
        self._tasks = [t for t in self._tasks if t.id != task.id]
    
    def list_tasks(self, project_id: int) -> List[Task]:
        return [task for task in self._tasks if task.project_id == project_id]
    
 # fake_unit_of_work.py

class FakeUnitOfWork:
    def __init__(self):
        self.repo = FakeRepository()
        self.committed = False
        self.session = self  # Fake Session

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass