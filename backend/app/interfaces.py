from abc import ABC,abstractmethod
from app.domain.user import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.user import User

class IUserRepository(ABC):
    @abstractmethod
    def save(self,user : "User") -> "User":
        """
        Accepts a pure Domain User object, persists it, 
        and returns the saved Domain User object.
        """
        pass

    @abstractmethod
    def get_by_email(self, email : str) -> User | None:
        """
        Retrieves a Domain User object by email if it exists,
        otherwise returns None.
        """
        pass