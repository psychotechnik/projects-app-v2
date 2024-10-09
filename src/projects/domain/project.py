from typing import Optional, List
from flask import jsonify

class Project:
    id: Optional[int]
    name: str
    description: Optional[str] = None
    tasks: List['Task'] = []
    
    def __init__(self, name, description):       
        self.name = name
        self.description = description
        self.tasks = []

    def __repr__(self):
        return f'<Project {self.name}>'
      
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,           
        }
        tasks = [task.to_dict() for task in self.tasks]
        if tasks: 
            data['tasks'] = tasks
        return data
    
