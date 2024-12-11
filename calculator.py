import streamlit as st
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

# Функция для проверки и парсинга чисел с пробелами или без
def parse_input(number_str):
    # Регулярное выражение для проверки формата (либо пробелы между группами, либо их отсутствие)
    if not re.match(r'^\d{1,3}( \d{3})*(\.\d+)?$|^\d+(\.\d+)?$', number_str.strip().replace(",", ".")):
        st.error("Некорректный формат числа! Используйте пробелы для разделения тысяч или вводите числа без пробелов.")
        return None
    try:
        # Удаляем пробелы и преобразуем запятую в точку
        normalized_number = number_str.replace(" ", "").replace(",", ".")
        return Decimal(normalized_number)
    except InvalidOperation:
        st.error("Введите корректное число!")
        return None

# Функция для форматирования вывода
def format_output(result):
    # Преобразование в строку с 6 знаками после запятой, округление математически
    result = result.quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)
    # Разбиение на группы тысяч и замена разделителей
    result_str = f"{result:,}".replace(",", " ").replace(".", ".")
    # Убираем незначащие нули в дробной части
    return result_str.rstrip("0").rstrip(".")

# Заголовок
st.title("Финансовый калькулятор")
st.markdown("#### Данькова Екатерина Григорьевна")
st.markdown("#### 3 курс 11 группа")
st.markdown("#### 2024")

# Поля для ввода чисел
num1_str = st.text_input("Введите первое число", value="0")
num2_str = st.text_input("Введите второе число", value="0")

# Выбор операции
operation = st.selectbox("Выберите операцию", ("Сложение", "Вычитание", "Умножение", "Деление"))

# Парсинг введённых чисел
num1 = parse_input(num1_str)
num2 = parse_input(num2_str)

if num1 is not None and num2 is not None:
    result = None
    try:
        # Выполнение выбранной операции
        if operation == "Сложение":
            result = num1 + num2
        elif operation == "Вычитание":
            result = num1 - num2
        elif operation == "Умножение":
            result = num1 * num2
        elif operation == "Деление":
            if num2 == 0:
                st.error("Ошибка: Деление на 0 невозможно!")
            else:
                result = num1 / num2

        # Проверка диапазона результата и вывод форматированного результата
        if result is not None:
            min_value = Decimal("-1000000000000.000000")
            max_value = Decimal("1000000000000.000000")

            if min_value <= result <= max_value:
                formatted_result = format_output(result)
                st.write(f"Результат: {formatted_result}")
            else:
                st.error("Результат выходит за пределы допустимого диапазона!")
    except InvalidOperation:
        st.error("Произошла ошибка при вычислении!")

