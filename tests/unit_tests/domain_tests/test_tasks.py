from projects.domain.task import Task

def test_task_to_dict_without_status():
    task_without_status = Task(project_id=1, name='Task 2', status=None)

    expected_dict_without_status = {
        'id': None,
        'name': 'Task 2',
    }

    assert task_without_status.to_dict() == expected_dict_without_status


def test_task_to_dict_with_status():
    task = Task(project_id=1, name='Task 1', status='In Progress')
    expected_dict = {
        'id': None,  # Assuming id is None for new tasks
        'name': 'Task 1',
        'status': 'In Progress'
    }

    assert task.to_dict() == expected_dict
    
