import streamlit as st
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN
import re

# Функция для проверки и парсинга чисел с пробелами или без
def parse_input(number_str):
    if not re.match(r'^-?\d{1,3}( \d{3})*(\.\d+)?$|^-?\d+(\.\d+)?$', number_str.strip().replace(",", ".")):
        st.error("Некорректный формат числа! Используйте пробелы для разделения тысяч или вводите числа без пробелов. Допускаются отрицательные числа.")
        return None
    try:
        normalized_number = number_str.replace(" ", "").replace(",", ".")
        return Decimal(normalized_number)
    except InvalidOperation:
        st.error("Некорректный формат числа! Используйте пробелы для разделения тысяч или вводите числа без пробелов. Допускаются отрицательные числа, например: -123 456.789")
        return None

# Функция для форматирования вывода
def format_output(result):
    result = result.quantize(Decimal('0.0000000000'), rounding=ROUND_HALF_UP)
    result_str = f"{result:,}".replace(",", " ").replace(".", ".")
    return result_str

# Функция вычислений
def calculate(number1, number2, number3, number4, op1, op2, op3):
    def get_result(num1, num2, operation):
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "/":
            if num2 == Decimal('0'):
                st.error("Ошибка: Деление на ноль невозможно!")
                return None
            return num1 / num2
        return None

    result1 = get_result(number2, number3, op2)
    if result1 is None:
        return None

    if op3 in ['*', '/'] and op1 in ['+', '-']:
        result2 = get_result(result1, number4, op3)
        if result2 is None:
            return None
        result3 = get_result(number1, result2, op1)
    else:
        result2 = get_result(number1, result1, op1)
        if result2 is None:
            return None
        result3 = get_result(result2, number4, op3)

    if result3 is not None:
        return result3.quantize(Decimal('1.000000'), rounding=ROUND_HALF_UP)
    return None

# Streamlit UI
st.title("Финансовый калькулятор")


st.sidebar.text("Данькова Екатерина Григорьевна\nКурс: 3\nГруппа: 11\nГод: 2024")
st.text("Число 1 x ( Число 2 x Число 3 ) x Число 4")

# Ввод чисел
number1_str = st.text_input("Число 1", value="0")
number2_str = st.text_input("Число 2", value="0")
number3_str = st.text_input("Число 3", value="0")
number4_str = st.text_input("Число 4", value="0")

# Парсинг введённых значений
number1 = parse_input(number1_str)
number2 = parse_input(number2_str)
number3 = parse_input(number3_str)
number4 = parse_input(number4_str)

# Выбор операций
operation1 = st.selectbox("Операция 1", ["+", "-", "*", "/"], index=0)
operation2 = st.selectbox("Операция 2", ["+", "-", "*", "/"], index=0)
operation3 = st.selectbox("Операция 3", ["+", "-", "*", "/"], index=0)

# Выбор округления
rounding_method = st.selectbox("Вид округления", ["математическое", "бухгалтерское", "усечение"], index=0)

if st.button("Вычислить"):
    if None in [number1, number2, number3, number4]:
        st.error("Введите корректные значения!")
    else:
        result = calculate(number1, number2, number3, number4, operation1, operation2, operation3)
        if result is not None:
            st.subheader(f"Результат: {format_output(result)}")

            if rounding_method == "математическое":
                rounded_result = result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            elif rounding_method == "бухгалтерское":
                rounded_result = result.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
            elif rounding_method == "усечение":
                rounded_result = result.quantize(Decimal('1'), rounding=ROUND_DOWN)

            st.subheader(f"Округлённый результат: {format_output(rounded_result)}")
