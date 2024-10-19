from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String, nullable=False)
    send_time = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages", lazy="selectin")
    chat = relationship("Chat", foreign_keys=[chat_id], back_populates="messages", lazy="selectin")
