from __future__ import annotations
from abc import ABC,abstractmethod
from app.domain.user import User
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.domain.user import User
    from app.domain.task import Task

class IUserRepository(ABC):
    @abstractmethod
    def save(self,user : "User") -> "User":
        """
        Accepts a pure Domain User object, persists it, 
        and returns the saved Domain User object.
        """
        pass

    @abstractmethod
    def get_by_email(self, email : str) -> "User" | None:
        """
        Retrieves a Domain User object by email if it exists,
        otherwise returns None.
        """
        pass


class ITasksRepository(ABC):
    @abstractmethod
    def save(self,task: "Task") -> "Task":
        pass

    @abstractmethod
    def get_by_id(self, task_id : uuid.UUID) -> "Task" | None:
        pass

    @abstractmethod
    def get_by_user(self, user_id : uuid.UUID) -> list["Task"]:
        pass 

    @abstractmethod
    def delete(self, task_id: uuid.UUID) -> bool:
        pass