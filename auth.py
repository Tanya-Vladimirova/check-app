from passlib.context import CryptContext

# Настройка шифрования (используем алгоритм bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """Превращает обычный пароль в защищенный хэш"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """Проверяет, совпадает ли введенный пароль с хэшем в базе"""
    return pwd_context.verify(plain_password, hashed_password)