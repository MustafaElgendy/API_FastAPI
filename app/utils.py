from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

#To vrtify password which user try to login with and the hashed password in db
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)