import requests
from fake_useragent import FakeUserAgent
import random


def remove_duplicates(input_file, output_file):
    # Открываем исходный файл для чтения
    with open(input_file, 'r', encoding='utf-8') as infile:
        # Читаем все строки файла
        lines = infile.readlines()

    # Используем set для удаления повторяющихся строк, сохраняя порядок
    seen = set()
    unique_lines = []

    for line in lines:
        # Если строка еще не встречалась, добавляем её в результат
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    # Открываем выходной файл для записи
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Записываем уникальные строки в новый файл
        outfile.writelines(unique_lines)


# Пример использования функции:
input_file = 'error.txt'  # Путь к входному файлу
output_file = 'error_1.txt'  # Путь к выходному файлу
remove_duplicates(input_file, output_file)



