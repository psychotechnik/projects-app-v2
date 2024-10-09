from projects.service_layer.projects import handlers
from projects.domain.project import Project
from . import FakeUnitOfWork


# Positive 

def test_create_project():
    uow = FakeUnitOfWork()
    project_data = {"name": "Test Project", "description": "Test Description"}
    
    handlers.create_project(**project_data, uow=uow)
    
    assert len(uow.repo.list_projects()) == 1
    project = uow.repo.list_projects()[0]
    assert project.name == project_data["name"]
    assert project.description == project_data["description"]
    assert uow.committed

def test_get_project():
    uow = FakeUnitOfWork()
    project = Project(name="Test Project", description="Test Description")
    
    uow.repo.create_project(project)
    
    retrieved_project = handlers.get_project(project.id, uow=uow)
    
    assert retrieved_project["name"] == "Test Project"
    assert retrieved_project["description"] == "Test Description"

def test_update_project():
    uow = FakeUnitOfWork()
    project = Project(name="Old Name", description="Old Description")
    
    uow.repo.create_project(project)
    
    handlers.update_project(project.id, "New Name", "New Description", uow=uow)
    
    updated_project = uow.repo.get_project(project.id)
    assert updated_project.name == "New Name"
    assert updated_project.description == "New Description"
    assert uow.committed

def test_delete_project():
    uow = FakeUnitOfWork()
    project = Project(name="Test Project", description="Test Description")
    
    uow.repo.create_project(project)
    
    handlers.delete_project(project.id, uow=uow)
    
    assert uow.repo.get_project(project.id) is None
    assert uow.committed
    
def test_list_projects_empty():
    uow = FakeUnitOfWork() 
    projects = handlers.list_projects(uow=uow) 

    assert projects == [] 
    
def test_list_projects_with_data():
    uow = FakeUnitOfWork() 

    uow.repo.create_project(Project(name="test-project-01", description="Test Project Description 1"))
    uow.repo.create_project(Project(name="test-project-02", description="Test Project Description 2"))
    uow.repo.create_project(Project(name="test-project-03", description="Test Project Description 3"))
    
    expected = [
        Project("test-project-01", "Test Project Description 1"),
        Project("test-project-02", "Test Project Description 2"),
        Project("test-project-03", "Test Project Description 3"),
    ]

    projects = handlers.list_projects(uow=uow) 

    for i in range(len(expected)):
        assert projects[i]["name"] == expected[i].name
        assert projects[i]["description"] == expected[i].description

# Negative
    
def test_get_nonexistent_project():
    uow = FakeUnitOfWork()
    
    project = handlers.get_project(999, uow=uow) 
    assert project is None  
    
def test_update_nonexistent_project():
    uow = FakeUnitOfWork()

    updated_project = handlers.update_project(999, "New Name", "New Description", uow=uow)
    
    assert updated_project is None
    assert not uow.committed

def test_delete_nonexistent_project():
    uow = FakeUnitOfWork()

    deleted_project = handlers.delete_project(999, uow=uow)
    
    assert deleted_project is None 
    assert not uow.committed  
