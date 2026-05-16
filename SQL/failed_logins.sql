-- Задача: Выявить потенциальный брутфорс (поиск всех неудачных попыток входа за сегодня)

-- 1. Создаем таблицу логов (как будто она уже существует в нашей SIEM-системе)
CREATE TABLE IF NOT EXISTS auth_logs (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50),
    ip_address VARCHAR(15),
    status VARCHAR(20),
    login_time TIMESTAMP
);

-- 2. Добавляем немного тестовых данных (имитация событий)
INSERT INTO auth_logs (username, ip_address, status, login_time) VALUES 
('admin', '192.168.1.10', 'SUCCESS', '2026-05-16 08:15:00'),
('guest', '10.0.0.5', 'FAILED', '2026-05-16 09:22:14'),
('root', '192.168.1.100', 'FAILED', '2026-05-16 10:05:01'),
('admin', '192.168.1.10', 'SUCCESS', '2026-05-16 11:30:00');

-- 3. Решение: SQL-запрос для аналитика SOC, который ищет подозрительную активность
SELECT username, ip_address, login_time 
FROM auth_logs 
WHERE status = 'FAILED'
ORDER BY login_time DESC;
