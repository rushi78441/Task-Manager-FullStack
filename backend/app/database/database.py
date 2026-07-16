from sqlalchemy import create_engine,Column,String,ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker,relationship
import uuid

# Production / Deployment local  storage string file layout
DATABASE_URL = "sqlite:///.TaskManager.db"

# connect args
engine = create_engine(url = DATABASE_URL, connect_args = {"check_same_thread" : False})
SessionLocal = sessionmaker(autoflush = False , bind = engine)
Base = declarative_base()


class SQLUserTable(Base):
    """
    Infrastructure Layer Data Model.
    This structure maps directly to physical database rows.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index= True, default=lambda : str(uuid.uuid4()))
    email = Column(String , unique=True, index=True,nullable=False)
    hashed_password = Column(String , nullable=False)
    
    ## relationship mappping back to tasks
    tasks = relationship("SQLTaskTable" , back_populates = "owner", cascade = "all, delete-orphan")


class SQLTaskTable(Base):
    __tablename__ = "tasks"

    task_id = Column(String , primary_key=True,index=True, default= lambda : str(uuid.uuid4()))
    task_title = Column(String, index=True , nullable= False)
    descryption = Column(String, default="")
    status = Column(String , default = "active" , nullable = False)
    user_id = Column(String, ForeignKey("users.id" , ondelete = "CASCADE"), nullable=False)

    # Relationship mapping back to the owing user
    owner = relationship("SQLUserTable", back_populates = "tasks")