#import sys
#import os
#import pytest

#sys.path.append(os.path.abspath(
#    os.path.join(os.path.dirname(__file__), '../src')))

#from projects.entrypoints.flask import create_app, db
#from projects.config import Config
#from projects.domain.user import User
#from projects.domain.project import Project
#from projects.domain.task import Task
#from projects.adapters.tasks.repository import SqlAlchemyTaskRepository

"""
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TOKEN_EXPIRES_IN = 3600  # Token lifetime (1 hour)

@pytest.fixture(scope='module')
def test_app():
    test_app = create_app(TestConfig)
    with test_app.app_context():
        db.create_all() 
        create_users()  
        create_projects_and_tasks()
        yield test_app
        db.session.remove()
        db.drop_all()  

@pytest.fixture(scope='function')
def client(test_app):
    with test_app.test_client() as client:
        db.session.commit()
        yield client
        db.session.remove() 
        
"""
# Positive Project Testing Scenarios

def param_get(request):
    return request.param

def test_get_projects(test_client, param_get):
    (username, password, expected_status_code) = param_get
    auth_header = get_token_auth_header(client, username, password)
    response = test_client.get('/api/projects', headers=auth_header)

    assert response.status_code == expected_status_code
    data = response.get_json()
    
    assert len(data) == 2  
    assert data[0]['name'] == "Test Project 1"
    assert data[1]['name'] == "Test Project 2"
    
def test_get_project_by_id(client, param_get):
    (username, password, expected_status_code) = param_get
    auth_header = get_token_auth_header(client, username, password)
    response = client.get('api/projects/1', headers=auth_header)
    
    assert response.status_code == expected_status_code
    data = response.get_json()
    assert data['name'] == "Test Project 1"
    

def test_create_project(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.post('/api/projects', json={
        'name': 'New Project',
        'description': 'New project description'
    }, headers=auth_header)
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'New Project'
    
def test_update_project(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.put('/api/projects/1', json={
        'name': 'Updated Project',
        'description': 'Updated description'
    }, headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Project'

def test_delete_project(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.delete('/api/projects/1', headers=auth_header)

    assert response.status_code == 204
    
# Negative Project Testing Scenarios

def test_get_project_not_found(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.get('/api/projects/999', headers=auth_header)
    
    assert response.status_code == 404
    
def test_create_project_unauthorized(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.post('/api/projects', json={
        'name': 'Unauthorized Project',
        'description': 'Unauthorized description'
    }, headers=auth_header)
    
    assert response.status_code == 403  

def test_update_project_unauthorized(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.put('/api/projects/1', json={
        'name': 'Unauthorized Update',
        'description': 'Unauthorized description'
    }, headers=auth_header)
    
    assert response.status_code == 403  

def test_delete_project_unauthorized(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.delete('/api/projects/1', headers=auth_header)
    
    assert response.status_code == 403  

def test_create_project_missing_data(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.post('/api/projects', json={}, headers=auth_header)
    
    assert response.status_code == 400  
    
# Positive Task Testing Scenarios

def test_get_tasks_for_project(client, param_get):
    (username, password, expected_status_code) = param_get
    auth_header = get_token_auth_header(client, username, password)
    response = client.get('/api/projects/1/tasks', headers=auth_header)
    
    assert response.status_code == expected_status_code
    data = response.get_json()
    
    assert len(data) == 2  
    assert data[0]['name'] == "Task 1 for Project 1"
    assert data[1]['status'] == "IN_PROGRESS"
    
def test_create_task(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.post('/api/projects/1/tasks', json={
        'name': 'New Task for Project 1',
        'status': 'NEW'
    }, headers=auth_header)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'New Task for Project 1'
    assert data['status'] == 'NEW'
    
def test_update_task_status(client):
    auth_header = get_token_auth_header(client, 'manager', 'manager_password')
    response = client.put('/api/projects/1/tasks/1', json={
        'status': 'COMPLETED'
    }, headers=auth_header)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'COMPLETED'
    
# Negative Task Testing Scenarios

def test_get_tasks_for_nonexistent_project(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.get('/api/projects/999/tasks', headers=auth_header)
    
    assert response.status_code == 404


def test_create_task_unauthorized(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.post('/api/projects/1/tasks', json={
        'name': 'Unauthorized Task',
        'status': 'NEW'
    }, headers=auth_header)
    
    assert response.status_code == 403
    
def test_update_task_status_unauthorized(client):
    auth_header = get_token_auth_header(client, 'employee', 'employee_password')
    response = client.put('/api/projects/1/tasks/1', json={
        'status': 'COMPLETED'
    }, headers=auth_header)
    
    assert response.status_code == 403
