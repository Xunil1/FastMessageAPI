from db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)      # Никнейм
    hash_password = Column(String, nullable=False)                          # Хэш пароля
    token = Column(String, default=None, nullable=True)                     # Токен
    telegram_id = Column(Integer, default=None, nullable=True)              # ID пользователя в телеграм

    chats = relationship('Chat', secondary='userchat', back_populates='users', lazy="selectin")
    sent_messages = relationship('Message', back_populates='sender', lazy="selectin")

