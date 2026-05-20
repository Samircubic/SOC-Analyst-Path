-- Задача: Анализ базовых логов авторизации (SQL-выборки)
-- В данном скрипте создается тестовая структура для хранения событий
-- и выполняются запросы для выявления аномальной активности.

-- 1. Создание таблицы (CREATE TABLE)
CREATE TABLE IF NOT EXISTS basic_logs (
    id INTEGER PRIMARY KEY,
    ip_address VARCHAR(20),
    action VARCHAR(50),
    status VARCHAR(20)
);

-- 2. Вставка данных (INSERT INTO)
-- Заполняем таблицу вручную
INSERT INTO basic_logs (ip_address, action, status) VALUES 
('192.168.1.10', 'LOGIN', 'SUCCESS'),
('10.0.0.5', 'LOGIN', 'FAILED'),
('10.0.0.5', 'LOGIN', 'FAILED'),
('10.0.0.5', 'LOGIN', 'FAILED'),
('8.8.8.8', 'DOWNLOAD', 'SUCCESS');

-- 3. Выборка данных с фильтром (SELECT + WHERE)
-- Ищем только неудачные попытки входа
SELECT ip_address, action 
FROM basic_logs 
WHERE status = 'FAILED';

-- 4. Группировка и подсчет (GROUP BY + COUNT + ORDER BY)
-- Считаем, сколько раз каждый IP фигурировал в логах, и сортируем по убыванию (от большего к меньшему)
SELECT ip_address, COUNT(*) as total_events
FROM basic_logs
GROUP BY ip_address
ORDER BY total_events DESC;
