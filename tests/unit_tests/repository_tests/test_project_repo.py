from sqlalchemy.sql import text
from projects.domain.project import Project
from projects.adapters.projects.repository import SqlAlchemyProjectRepository

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

# Creation Verification Test
def test_repository_can_save_a_project(db):
    # Create a new project instance
    project = Project(name="test-project-01", description="Test Project Description")
    repo = SqlAlchemyProjectRepository(db.session)  # Use the correct session
    # Save the project
    repo.create_project(project)
    db.session.commit()
    # Verify the project was saved in the db
    rows = db.session.execute(text("SELECT name, description FROM projects"))
    assert list(rows) == [("test-project-01", "Test Project Description")]
    
# Test for checking receipt by ID
def test_repository_can_retrieve_a_project(db):
    project_id = insert_project(db.session, "test-project-01", "Test Project Description")
    repo = SqlAlchemyProjectRepository(db.session)
    retrieved = repo.get_project(project_id)
    assert retrieved.id == project_id
    assert retrieved.name == "test-project-01"
    assert retrieved.description == "Test Project Description"
    
# Update Check Test    
def test_repository_can_update_a_project(db):
    project_id = insert_project(db.session, "test-project-01", "Old Description")
    repo = SqlAlchemyProjectRepository(db.session)
    project = repo.get_project(project_id)
    project.description = "Updated Description"
    repo.update_project(project)
    db.session.commit()

    updated_project = repo.get_project(project_id)
    
    assert updated_project.id == project_id
    assert updated_project.name == "test-project-01"
    assert updated_project.description == "Updated Description"
    
# Deletion Check Test
def test_repository_can_delete_a_project(db):
    project_id = insert_project(db.session, "test-project-01", "Test Project Description")
    repo = SqlAlchemyProjectRepository(db.session)
    project = repo.get_project(project_id)
    repo.delete_project(project)
    db.session.commit()

    deleted_project = repo.get_project(project_id)
    assert deleted_project is None
    
# Test of checking the receipt of the task list
def test_repository_can_list_projects(db):
    """    
    SQL does not guarantee exact ordering when joinedloads are used in a query. 
    When using SQLAlchemy joinedload, additional variations in the order of objects may appear 
    due to the internal workings of queries and join execution.
    """

    insert_project(db.session, "test-project-01", "Test Project Description 1")
    insert_project(db.session, "test-project-02", "Test Project Description 2")
    insert_project(db.session, "test-project-03", "Test Project Description 3")
    
    expected = [
        Project("test-project-01", "Test Project Description 1"),
        Project("test-project-02", "Test Project Description 2"),
        Project("test-project-03", "Test Project Description 3"),
    ]
    
    repo = SqlAlchemyProjectRepository(db.session)
    projects = repo.list_projects()
    
    for expected_project in expected:
        print(expected_project.name)
        assert any(
            project.name == expected_project.name 
            and 
            project.description == expected_project.description 
            for project in projects
        )
