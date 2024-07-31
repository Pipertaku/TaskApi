from passlib.context import CryptContext


pwd_password = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hashingpassword(password):
    return pwd_password.hash(password)

def verifypassword (plain_password, hashed_password):
    return pwd_password.verify(plain_password,hashed_password)

    




