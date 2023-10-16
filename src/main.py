from utils import *
# Получение данных из файла.
dict_list_operation = open_json("operations.json")
# Получение операций которые были выполнены.
complete_operations = receiving_completed_transactions(dict_list_operation)
# Сортировка операций по дате
sorted_operations_by_date = sort_by_date(complete_operations)
# Маскируем данные карт и счетов по операциям.
masking_number = hiding_numbers(sorted_operations_by_date)
# Форматирование даты для подготовки использования этих данных
formated_date = getting_date(sorted_operations_by_date)
formated_date.reverse()
# Получение данных для вывода пользователю
output_info = returning_data_to_the_user(formated_date)
# Вывод данных
for i in output_info:
    print(i)
