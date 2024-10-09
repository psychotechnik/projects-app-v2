from projects.service_layer.tasks import handlers 
from projects.domain.task import Task
from . import FakeUnitOfWork


# Positive 

def test_create_task(): 
    uow = FakeUnitOfWork()
    task_data = {"project_id": 1, "name": "Test Task", "status": "Pending"}
    
    handlers.create_task(**task_data, uow=uow)
    
    assert len(uow.repo.list_tasks(project_id=1)) == 1
    task = uow.repo.list_tasks(project_id=1)[0]
    assert task.name == task_data["name"]
    assert task.status == task_data["status"]
    assert task.project_id == task_data["project_id"]
    assert uow.committed

def test_get_task():
    uow = FakeUnitOfWork()
    task = Task(project_id=1, name="Test Task", status="Pending")
    
    uow.repo.create_task(task)
    
    retrieved_task = handlers.get_task(task.id, uow=uow)
    assert retrieved_task.name  == "Test Task"
    assert retrieved_task.status == "Pending"

def test_update_task_status():
    uow = FakeUnitOfWork()
    task = Task(project_id=1, name="Test Task", status="Pending")
    
    uow.repo.create_task(task)
    
    handlers.update_task_status(1, task.id, "Completed", uow=uow)
    
    updated_task = uow.repo.get_task(task.id)
    assert updated_task.status == "Completed"
    assert uow.committed

def test_get_tasks_for_project():
    uow = FakeUnitOfWork()

    uow.repo.create_task(Task(project_id=1, name="Task 1", status="Pending"))
    uow.repo.create_task(Task(project_id=1, name="Task 2", status="In Progress"))
    uow.repo.create_task(Task(project_id=1, name="Task 3", status="Pending"))
    
    expected = [
        Task(project_id=1, name="Task 1", status="Pending"),
        Task(project_id=1, name="Task 2", status="In Progress"),
        Task(project_id=1, name="Task 3", status="Pending")
    ]

    tasks = handlers.get_tasks_for_project(project_id=1, uow=uow)
     
    for i in range(len(expected)):
        assert tasks[i]["name"] == expected[i].name
        assert tasks[i]["status"] == expected[i].status
    

    # Negative
    
def test_get_nonexistent_task():
    uow = FakeUnitOfWork()
    
    task = handlers.get_task(999, uow=uow)
    assert task is None




