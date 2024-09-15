from passlib.context import CryptContext
# here we were defined  the type of algorithm using for our hashing password
# and  The value "auto" means that it will automatically handle deprecated
# schemes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
