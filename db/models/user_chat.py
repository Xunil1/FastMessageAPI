from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class UserChat(Base):
    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    chat_id = Column(Integer, ForeignKey('chat.id'))