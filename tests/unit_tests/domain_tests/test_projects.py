from projects.domain.project import Project
from projects.domain.task import Task

def test_project_to_dict_without_task():

    project = Project(name='Project 1', description='Test project')
    
    expected_dict = {
        'id': None,  # Assuming id is None for new projects
        'name': 'Project 1',
        'description': 'Test project',
    }
    
    assert project.to_dict() == expected_dict
    
def test_project_to_dict_with_task():
    
    project = Project(name='Project 1', description='Test project')
    task1 = Task(project_id=1, name='Task 1', status='In Progress')
    task2 = Task(project_id=1, name='Task 2', status=None)
    project.tasks = [task1, task2]

    expected_dict_with_tasks = {
        'id': None,
        'name': 'Project 1',
        'description': 'Test project',
        'tasks': [
            {'id': None, 'name': 'Task 1', 'status': 'In Progress'},
            {'id': None, 'name': 'Task 2'}
        ]
    }

    assert project.to_dict() == expected_dict_with_tasks