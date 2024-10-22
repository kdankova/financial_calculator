import streamlit as st
from decimal import Decimal, InvalidOperation
import locale

# Устанавливаем локальные настройки
locale.setlocale(locale.LC_NUMERIC, '')  # Региональные настройки
decimal_sep = locale.localeconv()['decimal_point']


def parse_input(number_str):
    try:
        number_str = number_str.replace(",", ".")  # Преобразуем запятую в точку
        return Decimal(number_str)
    except InvalidOperation:
        st.error("Введите корректное число!")
        return None


st.title("Финансовый калькулятор")
st.markdown("#### Данькова Екатерина Григорьевна")
st.markdown("#### 3 курс 11 группа")
st.markdown("#### 2024")

num1_str = st.text_input("Введите первое число", value="0")
num2_str = st.text_input("Введите второе число", value="0")

operation = st.selectbox("Выберите операцию", ("Сложение", "Вычитание"))

num1 = parse_input(num1_str)
num2 = parse_input(num2_str)

if num1 is not None and num2 is not None:
    result = None
    if operation == "Сложение":
        result = num1 + num2
    elif operation == "Вычитание":
        result = num1 - num2

    min_value = Decimal("-1000000000000.000000")
    max_value = Decimal("1000000000000.000000")

    if min_value <= result <= max_value:
        # Преобразуем результат в float и форматируем вывод с 6 знаками после запятой
        result_float = float(result)
        formatted_result = f"{result_float:.6f}"  # Ограничиваем до 6 знаков после запятой
        st.write(f"Результат: {formatted_result}")
    else:
        st.error("Результат выходит за пределы допустимого диапазона!")
