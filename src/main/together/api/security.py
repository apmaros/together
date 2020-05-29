from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha512"],
        default="pbkdf2_sha512",
        pbkdf2_sha512__default_rounds=30000
)


def encrypt(secret):
    return pwd_context.encrypt(secret)


def secret_is_valid(secret, hashed) -> bool:
    return pwd_context.verify(secret, hashed)
