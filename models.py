from sqlalchemy import Column, Integer, String, Boolean,TIMESTAMP, text ,ForeignKey
from sqlalchemy.sql.expression import null
from database import Base
from time import timezone
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, server_default="1", nullable=False)
    user_id = Column(Integer,ForeignKey('users.id', ondelete = 'CASCADE'),nullable=False )
    owner = relationship('User')
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable= False ,unique=True)
    password = Column(String(100),nullable = False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    phone_number = Column(String(100))
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key = True)
    post_id = Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key = True)
    