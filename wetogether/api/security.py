from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha512"],
        default="pbkdf2_sha512",
        pbkdf2_sha512__default_rounds=30000
)


def encrypt(password):
    return pwd_context.encrypt(password)


def verify_secret(password, hashed) -> bool:
    return pwd_context.verify(password, hashed)
