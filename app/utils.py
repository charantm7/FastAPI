from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hashed(password: str):
    return pwd_context.hash(password)

def verify(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)