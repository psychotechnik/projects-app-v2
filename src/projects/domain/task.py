from typing import Optional

class Task:
    id: Optional[int]
    project_id: int
    name: str
    status: Optional[str] = None
    project: Optional['Project'] = None 
    
    def __init__(self, project_id,  name, status):       
        self.project_id = project_id
        self.name = name
        self.status = status
        
    
    def __repr__(self):
        return f'<Task {self.name} - {self.status}>'
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,       
        }
        if self.status:
           data['status'] = self.status
        return data
