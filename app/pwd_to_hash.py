import bcrypt

def hash_password(pwd: str) -> str:
    hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt(rounds=10))
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


if __name__ == '__main__':
    pwd_hash = hash_password("test12")
    print(pwd_hash)