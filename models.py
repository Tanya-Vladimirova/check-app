from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # Это наш логин
    full_name = Column(String)                        # Имя пользователя
    hashed_password = Column(String)                  # Зашифрованный пароль