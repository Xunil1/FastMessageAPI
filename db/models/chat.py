from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Chat(Base):
    id = Column(Integer, primary_key=True, index=True)

    users = relationship('User', secondary='userchat', back_populates='chats', lazy="selectin")
    messages = relationship('Message', back_populates='chat', lazy="selectin")
