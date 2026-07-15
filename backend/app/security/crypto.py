import bcrypt


def hash_password(password : str) -> str:
    """
    Convert Plain test password into a secure, non-reversible cryptographic hash
    """

    # generate a random salt value and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed.decode('utf-8')


def verify_password(plain_password : str, hashed_password : str) -> bool:
    """
    Verifies if an incoming plain-text password matches the stored hash.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


