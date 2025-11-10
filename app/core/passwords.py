from pwdlib import PasswordHash

pwd_hasher = PasswordHash.recommended()


def get_password_hash(plain_password):
    return pwd_hasher.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_hasher.verify(plain_password, hashed_password)