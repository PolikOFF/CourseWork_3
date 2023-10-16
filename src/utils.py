import json
import os
from datetime import datetime


def open_json(filename):
    """
    Функция открывает файл json, в котором находятся списки словарей со следующими полями:
    - `id` — id транзакциии.
    - `date` — информация о дате совершения операции.
    - `state` — статус перевода:
        - `EXECUTED`  — выполнена,
        - `CANCELED`  — отменена.
    - `operationAmount` — сумма операции и валюта.
    - `description` — описание типа перевода.
    - `from` — откуда (может отсутстовать).
    - `to` — куда.
    Возвращает список операций формата python.
    :param filename: файл со списком словарей json.
    :return: список словарей формата python.
    """
    with open(os.path.join(filename), "r", encoding="utf-8") as file:
        dict_list_operation = json.load(file)
    return dict_list_operation


def receiving_completed_transactions(dict_list_operation):
    """
    Функция получает из общего списка операций,
    операции которые были выполнены(не отменены).
    :param dict_list_operation: исходный список словарей операций.
    :return: новый список с выполненными операциями.
    """
    list_dicts_of_completed_operations = []
    for operation_dictionary in dict_list_operation:
        if operation_dictionary == {}:
            continue
        else:
            if operation_dictionary["state"] == "EXECUTED":
                list_dicts_of_completed_operations.append(operation_dictionary)

    return list_dicts_of_completed_operations


def sort_by_date(list_operations):
    """
    Функция для сортировки списка выполненных операций по дате выполнения.
    :param list_operations: список словарей с операциями.
    :return: возваращает отсортированный список по дате выполнения.
    """
    sorted_list_operations_by_date = sorted(list_operations, key=lambda i: i["date"])
    return sorted_list_operations_by_date


def hiding_numbers(list_of_dictionaries):
    """Функция 'прячет' значения словарей с заданным форматом:

    - Номер карты замаскирован и не отображается целиком в формате  XXXX XX** **** XXXX (видны первые 6 цифр
     и последние 4, разбито по блокам по 4 цифры, разделенных пробелом).

    - Номер счета замаскирован и не отображается целиком в формате  **XXXX
    (видны только последние 4 цифры номера счета).

    :param list_of_dictionaries: список словарей с операциями.
    :return: возвращает список словарей в котором заменнены значения 'from' и 'to'.
    """
    for i in list_of_dictionaries:
        if "Счет" in i.setdefault("from", "Новый вклад"):
            i["from"] = "Счет **" + i["from"][-4:]
        elif "Счет" and "Новый вклад" not in i["from"]:
            i["from"] = (i["from"][:-16] + i["from"][-16:-12] + " " + i["from"][-12:-10]
                         + "** " + "****" + " " + i["from"][-4:])

    for i in list_of_dictionaries:
        if "Счет" in i["to"]:
            i["to"] = "Счет **" + i["to"][-4:]
        else:
            i["to"] = (i["to"][:-16] + i["to"][-16:-12] + " " + i["to"][-12:-10] + "** "
                       + "****" + " " + i["to"][-4:])

    return list_of_dictionaries


def getting_date(list_access_operation):
    """
    Функция меняет формат даты в значении словаря 'date'.
    :param list_access_operation: список словарей с операциями.
    :return: возвращает список словарей,
    в котором отредактировано значение 'date' под формат ДД.ММ.ГГГГ (пример: 14.10.2018).
    """
    for i in list_access_operation:
        date_operation = datetime.fromisoformat(i["date"])
        year = date_operation.year
        month = date_operation.month
        day = date_operation.day
        i["date"] = f"{day}.{month}.{year}"

    return list_access_operation


def returning_data_to_the_user(list_access_operation):
    """
    Функция формирует данные для вывода пользователю.
    :param list_access_operation: список выполненных операций
    :return: возвращает первые 5 операций с данными формата:
    14.10.2018 Перевод организации
    Visa Platinum 7000 79** **** 6361 -> Счет **9638
    82771.72 руб.
    """
    recent_transactions = []
    x = 0
    for i in list_access_operation:
        if x < 5:
            (recent_transactions.append
                (f'''{i["date"]} {i["description"]}
{i["from"]} -> {i["to"]}
{i["operationAmount"]["amount"]} {i["operationAmount"]["currency"]["name"]}\n'''))
            x += 1
    return recent_transactions
