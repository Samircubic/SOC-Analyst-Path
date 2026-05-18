# Задача 1: Найти пропущенное число в массиве (содержащем числа от 0 до n)
# Решение через математическую формулу суммы арифметической прогрессии
def missing_number(nums):
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum

# Задача 2: Валидация скобок (Valid Parentheses)
# Решение через стек (Stack)
def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack

if __name__ == "__main__":
    print(f"Тест Задачи 1 (Missing number in [3,0,1]): {missing_number([3,0,1])}")
    print(f"Тест Задачи 2 (Is '([{}])' valid?): {is_valid_parentheses('([{}])')}")
