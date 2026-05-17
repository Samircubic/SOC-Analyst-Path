"""
Инструкция: Работа с Base64 (Кодирование и декодирование).
Base64 — это способ превратить любые данные (картинки, файлы, символы) в простой текст (ASCII).
В SOC-аналитике это нужно знать ОЧЕНЬ хорошо, потому что хакеры постоянно используют Base64,
чтобы спрятать свои вредоносные команды от антивирусов (это называется Обфускация).
"""
import base64

def decode_hacker_command(encoded_string):
    # Декодируем из Base64 обратно в понятный текст
    # 1. b64decode переводит строку в байты
    # 2. decode('utf-8') переводит байты обратно в читаемый текст
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode('utf-8')

def encode_my_secret(secret_text):
    # Кодируем наш текст в Base64
    encoded_bytes = base64.b64encode(secret_text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

if __name__ == "__main__":
    print("[*] Анализ подозрительного скрипта...")
    
    # Симуляция: Мы нашли в логах веб-сервера подозрительную команду.
    # Для системного администратора это выглядит как бессмысленный набор букв.
    suspicious_payload = "cm0gLXJmIC8gIyA8LS0tIFZlcnkgYmFkIG1hbHdhcmUgY29tbWFuZA=="
    
    print(f"Найдена закодированная команда: {suspicious_payload}")
    
    # Аналитик SOC расшифровывает её, чтобы понять суть угрозы
    real_command = decode_hacker_command(suspicious_payload)
    print(f"[!!!] ВНИМАНИЕ! Расшифрованная команда хакера: {real_command}\n")
    
    # Практика: зашифруем свое собственное сообщение
    my_secret = "SOC Analyst is watching you"
    print(f"[+] Кодируем свое сообщение: '{my_secret}'")
    print(f"[+] Результат (Base64): {encode_my_secret(my_secret)}")
