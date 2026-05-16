"""
Инструкция: Парсер логов (Извлечение IP-адресов).
В работе SOC-аналитика постоянно приходится анализировать огромные "сырые" текстовые логи.
Этот скрипт использует регулярные выражения (RegEx) для поиска всех IPv4-адресов 
в тексте лога, а затем подсчитывает, с какого IP было больше всего запросов.
Это самый базовый шаг для выявления аномалий, DDoS-атак или перебора паролей (Brute-force).
"""
import re
from collections import Counter

def extract_and_analyze_ips(log_data):
    # Регулярное выражение (RegEx) для поиска IPv4 адреса
    # Ищет паттерн: от 1 до 3 цифр, разделенных точками (X.X.X.X)
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    # re.findall находит все совпадения с паттерном в тексте лога
    found_ips = re.findall(ip_pattern, log_data)
    
    # Counter автоматически считает, сколько раз каждый IP встретился в списке
    ip_counts = Counter(found_ips)
    
    return ip_counts

if __name__ == "__main__":
    # Имитация сырого лога веб-сервера (например, Nginx или Apache)
    sample_logs = """
    192.168.1.10 - - [16/May/2026:10:00:01] "GET /index.html HTTP/1.1" 200
    10.0.0.5 - - [16/May/2026:10:00:05] "POST /login HTTP/1.1" 401
    10.0.0.5 - - [16/May/2026:10:00:06] "POST /login HTTP/1.1" 401
    10.0.0.5 - - [16/May/2026:10:00:07] "POST /login HTTP/1.1" 401
    172.16.0.50 - - [16/May/2026:10:01:00] "GET /images/logo.png HTTP/1.1" 200
    10.0.0.5 - - [16/May/2026:10:01:05] "POST /login HTTP/1.1" 401
    """
    
    print("[*] Анализ логов начат...\n")
    results = extract_and_analyze_ips(sample_logs)
    
    print("Топ IP-адресов по количеству запросов:")
    print("-" * 40)
    
    # Выводим все IP и количество их упоминаний (most_common сортирует по убыванию)
    for ip, count in results.most_common():
        # Если с одного IP было больше 3 запросов, помечаем его как подозрительный
        if count > 3:
            print(f"[!!!] ВНИМАНИЕ: {ip} замечен {count} раз(а)! Возможен Brute-force.")
        else:
            print(f"[+] {ip}: {count} запрос(ов)")
