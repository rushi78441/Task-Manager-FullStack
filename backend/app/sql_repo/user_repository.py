from sqlalchemy.orm import Session
import uuid
from app.interfaces import IUserRepository
from app.domain.user import User
from app.database.database import SQLUserTable


class SQLUserRepository(IUserRepository):
    def __init__(self, db_session : Session):
        self.db = db_session

    def save(self, user : User) -> User:
        """
        Translates a pure decoupled Object-Oriented Domain object 
        into an infrastructure database row structure and commits it.
        """

        db_user = SQLUserTable(
            id = str(user.id),
            email = user.email,
            hashed_password = user.hashed_password
        )

        # adding user in db
        self.db.add(db_user)
        self.db.commit()    # commit changes
        self.db.refresh(db_user)    # refresh db user 
        return user
    
    def get_by_email(self, email: str) -> str:
        """
        Retrive User object by email filtering in User Tabel Database
        """
        # filter user_db from UserTabel Db
        db_user = self.db.query(SQLUserTable).filter(SQLUserTable.email == email).first()

        if not db_user:
            return None
        
        return User(
            id = uuid.UUID(db_user.id),
            email = db_user.email,
            hashed_password = db_user.hashed_password
        )

