from app.interfaces import ITasksRepository
from app.domain.task import Task
from app.database.database import SQLTaskTable
from sqlalchemy.orm import Session
import uuid


class SQLTaskRepository(ITasksRepository):
    def __init__(self,db: Session):
        self.db = db

    def save(self, task: Task) -> Task:
        # Check if task record already exists for update , otherwise add new row
        task_db = self.db.query(SQLTaskTable).filter(SQLTaskTable.task_id == str(task.task_id)).first()

        # If task not found , we add one
        if not task_db:
            task_db = SQLTaskTable(
                task_id = str(task.task_id),
                task_title = task.task_title,
                descryption = task.descryption,
                status = task.status,
                user_id = str(task.user_id)
            )

            # add in db
            self.db.add(task_db)

        # else task found in db, we will update its title and descryption
        else:
            task_db.task_title = task.task_title
            task_db.descryption = task.descryption
            task_db.status = task.status

        ## Commit changes in DB And refresh page
        self.db.commit()
        self.db.refresh(task_db)

        # Map and return Db model back to core domain entity model
        return Task(
            task_id = uuid.UUID(task_db.task_id),
            task_title = task_db.task_title,
            descryption = task_db.descryption,
            status = task_db.status,
            user_id = uuid.UUID(task_db.user_id)
        )
    

    def get_by_id(self, task_id : uuid.UUID) -> Task | None:
        
        # find task by id
        task_db = self.db.query(SQLTaskTable).filter(SQLTaskTable.task_id == str(task_id)).first()

        if not task_db:
            return None
        
        return Task(
            task_id = uuid.UUID(task_db.task_id),
            task_title = task_db.task_title,
            descryption = task_db.descryption,
            status = task_db.status,
            user_id = uuid.UUID(task_db.user_id)
        )
    
    def get_by_user(self, user_id: uuid.UUID) -> list[Task]:
        # filter all tasks of user by user id
        tasks = self.db.query(SQLTaskTable).filter(SQLTaskTable.user_id == str(user_id)).all()

        if not tasks:
            return []

        ## return tasks in a list by smart for loop
        return [
            Task(
                task_id = uuid.UUID(t.task_id),
                task_title = t.task_title,
                descryption = t.descryption,
                status = t.status,
                user_id = uuid.UUID(t.user_id)
            ) for t in tasks
        ]
    

    def delete(self, task_id: uuid.UUID) -> bool:
        # find task to delete by task id
        task = self.db.query(SQLTaskTable).filter(SQLTaskTable.task_id == str(task_id)).first()

        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()

        return True