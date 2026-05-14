"""
Инструкция: Простой сканер портов на Python.
Проверяет доступность списка портов на удаленном хосте.
Полезно для базовой разведки (Reconnaissance) в сетях и проверки безопасности.
"""
import socket

def scan_port(ip, port):
    # Создаем сокет с таймаутом 1 секунда, чтобы скрипт не завис надолго
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    # Пытаемся подключиться: connect_ex возвращает 0, если порт открыт
    result = sock.connect_ex((ip, port))
    
    if result == 0:
        print(f"[+] Порт {port} на {ip} ОТКРЫТ")
    else:
        print(f"[-] Порт {port} на {ip} ЗАКРЫТ (или фильтруется)")
        
    sock.close()

if __name__ == "__main__":
    target_ip = "8.8.8.8" # Публичный DNS-сервер Google
    ports_to_check = [53, 80, 443, 22] # DNS, HTTP, HTTPS, SSH
    
    print(f"Запуск сканирования хоста {target_ip}...")
    for p in ports_to_check:
        scan_port(target_ip, p)
