"""
Инструкция: Простой генератор случайных MAC-адресов.
Иногда в сетях (или при пентесте) нужно временно подменить свой MAC-адрес (MAC Spoofing),
чтобы обойти фильтры на роутерах, бесплатном Wi-Fi или скрыть свое устройство.
Этот скрипт генерирует локальный (unicast) MAC-адрес случайным образом.
"""
import random

def generate_random_mac(oui_prefix=None):
    # Если передан префикс вендора (OUI), используем его (например, префикс Apple)
    # Если нет, используем стандартный префикс локального адреса [0x02]
    if oui_prefix and len(oui_prefix) == 3:
        mac = list(oui_prefix)
    else:
        mac = [0x02] 
    
    # Генерируем недостающие байты (всего в MAC должно быть 6 байт)
    bytes_to_generate = 6 - len(mac)
    for _ in range(bytes_to_generate):
        mac.append(random.randint(0x00, 0xff))
        
    # Форматируем в привычный вид: XX:XX:XX:XX:XX:XX
    return ':'.join(f'{b:02x}' for b in mac)

if __name__ == "__main__":
    # Генерируем обычный локальный случайный MAC
    new_mac = generate_random_mac()
    print(f"[~] Обычный случайный MAC: {new_mac}")
    
    # Новая фича: генерируем MAC-адрес, который будет притворяться устройством от Apple (OUI: 00:25:00)
    apple_mac = generate_random_mac(oui_prefix=[0x00, 0x25, 0x00])
    print(f"[~] MAC-адрес, маскирующийся под Apple: {apple_mac}")
