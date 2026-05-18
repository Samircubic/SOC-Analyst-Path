"""
Инструкция: Детектор фишинговых доменов (Typo-squatting).
В SOC часто приходится анализировать ссылки из спам-писем (Phishing).
Хакеры регистрируют домены, очень похожие на настоящие (например, "g00gle.com" или "sberbannk.ru"),
чтобы обмануть пользователей. 
Этот скрипт использует математический алгоритм "Расстояние Левенштейна", 
чтобы вычислить, насколько один домен похож на другой, и предупреждает об опасности.
"""

def levenshtein_distance(s1, s2):
    # Вычисляет минимальное количество изменений (вставок, удалений, замен),
    # чтобы превратить строку s1 в s2. Классический алгоритм компьютерной лингвистики.
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        
    return previous_row[-1]

def check_domain_safety(suspicious_domain, legitimate_domains):
    print(f"[*] Анализируем URL: {suspicious_domain}")
    
    for legit in legitimate_domains:
        distance = levenshtein_distance(suspicious_domain, legit)
        
        # Если разница всего в 1 или 2 символа, это очень подозрительно!
        if distance == 0:
            print(f"[+] Домен безопасен: {suspicious_domain} (Оригинал)")
            return
        elif distance <= 2:
            print(f"[!!!] УГРОЗА ФИШИНГА: '{suspicious_domain}' маскируется под '{legit}'!")
            return
            
    print(f"[-] Домен '{suspicious_domain}' не похож на известные бренды (скорее всего обычный сайт).")

if __name__ == "__main__":
    # База легитимных доменов, которые мы "защищаем" (Белый список)
    trusted_brands = ["google.com", "yandex.ru", "vk.com", "sberbank.ru"]
    
    # Симуляция: тестируем различные ссылки, найденные в корпоративной почте
    urls_to_test = [
        "g00gle.com",        # Фишинг (замена o на 0)
        "yandex.ru",         # Легитимный
        "sberbannk.ru",      # Фишинг (добавлена лишняя буква 'n')
        "random-site.org"    # Обычный левый сайт, не фишинг под наши бренды
    ]
    
    print("--- ЗАПУСК ДЕТЕКТОРА ФИШИНГА ---")
    for url in urls_to_test:
        check_domain_safety(url, trusted_brands)
        print("-" * 40)
