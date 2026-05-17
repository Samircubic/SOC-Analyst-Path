"""
Инструкция: Базовое хеширование и "взлом" паролей (Hashing & Cracking).
В кибербезопасности пароли никогда не хранятся в базах данных в открытом виде.
Они прогоняются через криптографическую функцию (например, SHA-256), которая выдает "хеш".
Этот скрипт показывает:
1. Как система превращает пароль в нечитаемый хеш.
2. Как хакеры с помощью атаки по словарю (Dictionary Attack) пытаются "взломать" украденные хеши.
"""
import hashlib

def hash_password(password):
    # Превращаем строку в байты и вычисляем SHA-256 хеш. 
    # Хеш невозможно "расшифровать" обратно математически.
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def dictionary_attack(target_hash, dictionary):
    print("[*] Запуск атаки по словарю (Dictionary Attack)...")
    for word in dictionary:
        # Хакер хеширует каждое слово из своего словаря и сравнивает с украденным хешем
        if hash_password(word) == target_hash:
            return word
    return None

if __name__ == "__main__":
    # 1. Симуляция: Пользователь регистрируется с очень слабым паролем
    weak_password = "qwerty"
    saved_hash = hash_password(weak_password)
    
    print(f"[Сервер] Пользователь создал пароль.")
    print(f"[Сервер] В базе данных сохранился хеш:\n{saved_hash}\n")
    
    # 2. Симуляция: Базу данных украли хакеры. У них есть только хеш, но нет пароля.
    # Они берут список самых популярных паролей (словарь) скачанный из интернета.
    hacker_dictionary = ["123456", "password", "admin", "qwerty", "iloveyou"]
    
    # Пытаются подобрать
    cracked_password = dictionary_attack(saved_hash, hacker_dictionary)
    
    if cracked_password:
        print(f"[!!!] УСПЕХ ХАКЕРА: Пароль подобран! Это: '{cracked_password}'")
    else:
        print("[-] Пароль безопасен, в словаре хакера его нет.")
