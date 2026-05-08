from cryptography.fernet import Fernet, InvalidToken
from app.crypto.key_manager import get_encryption_key


def get_fernet() -> Fernet:
    return Fernet(get_encryption_key())


def encrypt_field(value: str) -> str:
    if not value:
        return value
    f = get_fernet()
    encrypted = f.encrypt(value.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt_field(encrypted_value: str) -> str:
    if not encrypted_value:
        return encrypted_value
    try:
        f = get_fernet()
        decrypted = f.decrypt(encrypted_value.encode("utf-8"))
        return decrypted.decode("utf-8")
    except InvalidToken:
        return "[ПОМИЛКА РОЗШИФРУВАННЯ --- невірний ключ]"