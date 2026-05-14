"""
Инструкция: Скрипт простого TCP-клиента.
Он подключается к указанному хосту и порту (по умолчанию google.com:80),
отправляет простой HTTP-запрос и выводит полученный ответ.
Помогает понять основы работы с сокетами в Python.
"""
import socket

def run_client():
    target_host = "www.google.com"
    target_port = 80

    # Создаем socket (AF_INET - IPv4, SOCK_STREAM - TCP)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Подключаемся к хосту
    client.connect((target_host, target_port))
    
    # Отправляем данные (минимальный HTTP GET запрос)
    request = b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
    client.send(request)
    
    # Получаем часть ответа (до 4096 байт)
    response = client.recv(4096)
    
    # Декодируем байты в строку и выводим
    print("Ответ сервера:")
    print(response.decode(errors='ignore'))
    
    # Закрываем соединение
    client.close()

if __name__ == "__main__":
    run_client()
