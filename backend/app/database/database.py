from sqlalchemy import create_engine,Column,String
from sqlalchemy.orm import declarative_base,sessionmaker
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
    