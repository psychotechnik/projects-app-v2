import pytest
from projects.domain.project import Project
from projects.domain.task import Task
from projects.service_layer.projects.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy import text

class MyException(Exception):
        pass

# Helper function for creating a project
def insert_project(session, name, description):
    session.execute(
        text(f"INSERT INTO projects (name, description) VALUES ('{name}', '{description}')")
    )
    [[project_id]] = session.execute(
        text("SELECT id FROM projects WHERE name=:name AND description=:description"),
        dict(name=name, description=description),
    )
    return project_id

# Function to insert task directly into the database via SQLAlchemy session
def insert_task(session, project_id, name, status):
    """Insert a task directly into the database"""
    session.execute(
        text("INSERT INTO tasks (project_id, name, status) VALUES (:project_id, :name, :status)"),
        dict(project_id=project_id, name=name, status=status),
    )

# Test if a project can be retrieved and a task created using UnitOfWork
def test_uow_can_retrieve_project_and_task(db):
    session = db.session()
    insert_project(session, "Test Project", "Test Project Description")
    session.commit()

    uow = SqlAlchemyUnitOfWork(session_factory=db.session)
    with uow:
        proj = uow.repo.list_projects()[0]
        
        assert proj.name ==  "Test Project"
        assert proj.description == "Test Project Description"
        
        insert_task(uow.session, proj.id, "Task1", "Not Started")
        uow.commit()
        
        task = uow.session.query(Task).filter_by(name="Task1").one()
        assert task.project_id == proj.id
        assert task.status == "Not Started"
        
# Test if UnitOfWork rolls back uncommitted work by default
def test_rolls_back_uncommitted_work_by_default(db):
    uow = SqlAlchemyUnitOfWork(session_factory=db.session)
    with uow:
        project_id = insert_project(uow.session, "Project2", "Another Project")
        insert_task(uow.session, project_id, "Task2", "In Progress")
        # No commit here

    # Verify that the no task
    new_uow = SqlAlchemyUnitOfWork(session_factory=db.session)
    with new_uow:
        tasks = new_uow.session.query(Task).filter_by(name="Task2").all()
        assert tasks == []  # Task should not be found
        
# Test if UnitOfWork properly rolls back on errors
def test_rolls_back_on_error(db):
    uow = SqlAlchemyUnitOfWork(session_factory=db.session)
    with pytest.raises(MyException):
        with uow:
            project_id = insert_project(uow.session, "Project3", "Test Rollback")
            insert_task(uow.session, project_id, "Task3", "Completed")
            raise MyException()  # Simulate an error
    
    # Verify that neither the project nor the task was committed
    new_uow = SqlAlchemyUnitOfWork(session_factory=db.session)
    with new_uow:
        projects = new_uow.session.query(Project).filter_by(name="Project3").all()
        tasks = new_uow.session.query(Task).filter_by(name="Task3").all()

        assert projects == []  
        assert tasks == [] 