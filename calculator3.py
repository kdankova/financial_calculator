import streamlit as st
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN
import re

# Функция для проверки и парсинга чисел с пробелами или без
def parse_input(number_str):
    if not re.match(r'^\d{1,3}( \d{3})*(\.\d+)?$|^\d+(\.\d+)?$', number_str.strip().replace(",", ".")):
        st.error("Некорректный формат числа! Используйте пробелы для разделения тысяч или вводите числа без пробелов.")
        return None
    try:
        normalized_number = number_str.replace(" ", "").replace(",", ".")
        return Decimal(normalized_number)
    except InvalidOperation:
        st.error("Введите корректное число!")
        return None

# Функция для форматирования вывода
def format_output(result):
    result = result.quantize(Decimal('0.0000000000'), rounding=ROUND_HALF_UP)
    result_str = f"{result:,}".replace(",", " ").replace(".", ".")
    return result_str

# Функция для округления до целых по разным методам
def round_result(result, method):
    if method == "Математическое":
        return result.to_integral_value(rounding=ROUND_HALF_UP)
    elif method == "Бухгалтерское":
        return result.to_integral_value(rounding=ROUND_HALF_EVEN)
    elif method == "Усечение":
        return result.to_integral_value(rounding=ROUND_DOWN)
    return None

# Заголовок
st.title("Финансовый калькулятор")
st.markdown("#### Данькова Екатерина Григорьевна")
st.markdown("#### 3 курс 11 группа")
st.markdown("#### 2024")

# Горизонтальный ввод чисел и операций
col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 3, 2, 3, 2, 3])

with col1:
    num1_str = st.text_input("Число 1", value="0")
with col2:
    operation1 = st.selectbox("Операция 1", ["+", "-", "*", "/"])
with col3:
    num2_str = st.text_input("Число 2", value="0")
with col4:
    operation2 = st.selectbox("Операция 2 (приоритет)", ["+", "-", "*", "/"])
with col5:
    num3_str = st.text_input("Число 3", value="0")
with col6:
    operation3 = st.selectbox("Операция 3", ["+", "-", "*", "/"])
with col7:
    num4_str = st.text_input("Число 4", value="0")

# Парсинг чисел
num1 = parse_input(num1_str)
num2 = parse_input(num2_str)
num3 = parse_input(num3_str)
num4 = parse_input(num4_str)

if all(x is not None for x in [num1, num2, num3, num4]):
    try:
        # Промежуточное вычисление: num2 (op2) num3
        intermediate_result = None
        if operation2 == "+":
            intermediate_result = num2 + num3
        elif operation2 == "-":
            intermediate_result = num2 - num3
        elif operation2 == "*":
            intermediate_result = num2 * num3
        elif operation2 == "/":
            if num3 == 0:
                st.error("Ошибка: Деление на 0 невозможно!")
            else:
                intermediate_result = num2 / num3

        if intermediate_result is not None:
            intermediate_result = intermediate_result.quantize(Decimal('0.0000000000'), rounding=ROUND_HALF_UP)

        # Основное вычисление: num1 (op1) intermediate_result
        final_result = None
        if intermediate_result is not None:
            if operation1 == "+":
                final_result = num1 + intermediate_result
            elif operation1 == "-":
                final_result = num1 - intermediate_result
            elif operation1 == "*":
                final_result = num1 * intermediate_result
            elif operation1 == "/":
                if intermediate_result == 0:
                    st.error("Ошибка: Деление на 0 невозможно!")
                else:
                    final_result = num1 / intermediate_result

            # Последнее вычисление: final_result (op3) num4
            if final_result is not None:
                if operation3 == "+":
                    final_result = final_result + num4
                elif operation3 == "-":
                    final_result = final_result - num4
                elif operation3 == "*":
                    final_result = final_result * num4
                elif operation3 == "/":
                    if num4 == 0:
                        st.error("Ошибка: Деление на 0 невозможно!")
                    else:
                        final_result = final_result / num4

                # Проверка диапазона
                max_value = Decimal("1000000000000.0000000000")
                if abs(final_result) > max_value:
                    st.error("Переполнение! Результат выходит за пределы диапазона.")
                else:
                    st.write(f"Результат вычисления: {format_output(final_result)}")

                    # Выбор вида округления
                    rounding_method = st.radio("Выберите вид округления результата", ("Математическое", "Бухгалтерское", "Усечение"))
                    rounded_result = round_result(final_result, rounding_method)
                    st.write(f"Округленный результат: {rounded_result}")
    except InvalidOperation:
        st.error("Произошла ошибка при вычислении!")
