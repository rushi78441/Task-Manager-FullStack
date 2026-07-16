import uuid 
from app.interfaces import ITasksRepository

class Task():
    def __init__(self,
                task_title : str,
                descryption: str,
                user_id: uuid.UUID,
                task_id: uuid.UUID = None,
                status: str = "active"
                ):
        
        # if task tile is empty white space
        if not task_title.strip():
            raise ValueError("Task Title cannot be empty")
        
        # If task status is invalid
        if status not in ["active" , "completed"]:
            raise ValueError("Task Status must be in either 'active' or 'completed' ")
        
        self.task_id = task_id or uuid.uuid4()
        self.user_id = user_id
        self.task_title = task_title
        self.descryption = descryption
        self.status = status
    
    def complete(self):
        """Domain Action: Transition status to completed."""
        self.status = "completed"

    def activate(self):
        """Domain Action: Transition status to Active."""
        self.status = "active"