from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("Згенерований ключ Fernet:")
print(f"ENCRYPTION_KEY={key.decode()}")
print()
print("Цей ключ --- єдиний спосіб розшифрувати дані.")
print("Втрата ключа = втрата всіх зашифрованих даних.")