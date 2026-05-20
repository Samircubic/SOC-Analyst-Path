"""
Проект: Инструмент парсинга и анализа логов (SOC Log Analyzer & Database Builder)

ОПИСАНИЕ:
Скрипт предназначен для нормализации сырых текстовых логов и их загрузки в 
ин-мемори базу данных SQLite для последующего автоматизированного SQL-анализа.

СЦЕНАРИЙ ИСПОЛЬЗОВАНИЯ: 
Инструмент выполняет первичную обработку логов: разбивает строки на структурные поля, 
создает реляционную модель данных и выполняет выборки для выявления 
инцидентов информационной безопасности (например, признаков брутфорс-атак).
"""

import sqlite3

def setup_database(cursor):
    """Функция для создания таблицы в базе данных."""
    print("[*] Шаг 1: Создание базы данных и таблицы...")
    
    # Сначала удаляем таблицу, если она существует (для идемпотентности скрипта)
    cursor.execute("DROP TABLE IF EXISTS security_events")
    
    # Создаем схему данных для хранения событий
    create_table_sql = """
    CREATE TABLE security_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source_ip TEXT,
        action TEXT,
        status TEXT
    )
    """
    cursor.execute(create_table_sql)
    print("[+] Таблица 'security_events' успешно создана.\n")

def parse_and_insert_logs(cursor, raw_logs):
    """Функция для чтения текста и записи его в базу данных."""
    print("[*] Шаг 2: Чтение логов и запись в базу данных...")
    
    # Разбиваем большой текст на список отдельных строк по символу переноса строки (\n)
    lines = raw_logs.split('\n')
    
    inserted_count = 0
    
    # Обрабатываем лог построчно
    for line in lines:
        # Убираем лишние невидимые пробелы по краям
        line = line.strip()
        
        # Если строка пустая - просто пропускаем ее и идем к следующей
        if line == "":
            continue
            
        # Мы знаем, что в нашем логе формат такой: "Время IP Действие Статус"
        # Поэтому просто разделяем строчку по пробелам
        parts = line.split(" ")
        
        # Проверяем: если в строке ровно 4 слова, значит это правильный лог, работаем с ним
        if len(parts) == 4:
            log_time = parts[0]
            log_ip = parts[1]
            log_action = parts[2]
            log_status = parts[3]
            
            # Подготавливаем параметризованный запрос для вставки нормализованных данных
            # Параметризация (?) защищает от SQL-инъекций
            insert_sql = """
            INSERT INTO security_events (timestamp, source_ip, action, status)
            VALUES (?, ?, ?, ?)
            """
            
            # Выполняем SQL и передаем туда наши 4 переменные
            cursor.execute(insert_sql, (log_time, log_ip, log_action, log_status))
            inserted_count += 1
            
    print(f"[+] Успешно обработано и сохранено событий в БД: {inserted_count}\n")

def run_security_analysis(cursor):
    """Функция, которая делает SQL-запросы к нашей базе и печатает результаты."""
    print("[*] Шаг 3: Анализ данных (Запуск SQL-запросов к БД)...")
    print("-" * 60)
    
    # --- ЗАПРОС 1: Выявление неудачных попыток доступа ---
    print(">>> Поиск неудачных действий (FAILED):")
    query_failed = """
    SELECT timestamp, source_ip, action 
    FROM security_events 
    WHERE status = 'FAILED'
    """
    cursor.execute(query_failed)
    failed_rows = cursor.fetchall() # Забираем все найденные строки
    
    # Простой цикл для вывода каждого найденного результата
    for row in failed_rows:
        print(f"  - В {row[0]} с IP {row[1]} зафиксирован FAILED (Действие: {row[2]})")
    print()
    
    # --- ЗАПРОС 2: Топ IP-адресов (GROUP BY + COUNT) ---
    print(">>> Топ IP-адресов по активности (Ищем спам или брутфорс):")
    query_top_ips = """
    SELECT source_ip, COUNT(*) as total
    FROM security_events
    GROUP BY source_ip
    ORDER BY total DESC
    """
    cursor.execute(query_top_ips)
    top_ips_rows = cursor.fetchall()
    
    # Простой цикл с условием: если запросов больше 2-х, бьем тревогу
    for row in top_ips_rows:
        ip = row[0]
        count = row[1]
        
        if count > 2:
            print(f"  - [!!! ВНИМАНИЕ !!!] IP: {ip} -> Запросов: {count} (Слишком много!)")
        else:
            print(f"  - [OK] IP: {ip} -> Запросов: {count}")
            
    print("-" * 60)
    print("[+] Отчет по безопасности завершен!")

if __name__ == "__main__":
    import os
    # Читаем сырой лог из внешнего текстового файла
    # Используем os.path для корректного поиска файла независимо от того, откуда запущен скрипт
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Данные', 'soc_analyzer_logs.txt')
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_log_data = f.read()
    except FileNotFoundError:
        print(f"[-] Файл данных не найден: {file_path}")
        exit(1)
    
    # Подключаемся к базе данных SQLite. 
    # ':memory:' означает, что база создается прямо в оперативной памяти компьютера
    # и удалится после закрытия скрипта (очень удобно для тренировок).
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Запуск пайплайна обработки данных
    setup_database(cursor)
    parse_and_insert_logs(cursor, raw_log_data)
    run_security_analysis(cursor)
    
    # Обязательно закрываем соединение в конце
    conn.close()
