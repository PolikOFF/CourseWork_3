from src.utils import *


def test_receiving_completed_transactions():
    assert receiving_completed_transactions([{"state": "CANCEL"}, {"state": "EXECUTED"}]) == [{"state": "EXECUTED"}]
    assert receiving_completed_transactions([{}]) == []
    assert receiving_completed_transactions([{}, {}, {"state": "EXECUTED"}]) == [{"state": "EXECUTED"}]


def test_sort_by_date():
    assert (sort_by_date([{"date": "2019-08-26T10:50:58.294041", "A": "1"}, {"date": "26-08-2020T10:10", "B": "2"}])
            == [{"date": "2019-08-26T10:50:58.294041", "A": "1"}, {"date": "26-08-2020T10:10", "B": "2"}])


def test_hiding_numbers():
    assert hiding_numbers([
                           {"from": "Счет 12345684561235468795", "to": "МИР 1234123412344567"},
                           {"date": "20-20-2020", "to": "Счет 12345684561235468"}]) == [
                           {'from': 'Счет **8795', 'to': 'МИР 1234 12** **** 4567'},
                           {'date': '20-20-2020', 'from': 'Новый вклад', 'to': 'Счет **5468'}]
    assert hiding_numbers([{"from": "Visa CLassic 1234432112341234", "to": "Счет 12341234123412341234"}]) == [
                         {"from": "Visa CLassic 1234 43** **** 1234", "to": "Счет **1234"}]


def test_getting_date():
    assert getting_date([{"date": "2021-05-01", "test": "123"}, {"date": "2012-10-11T11:20", "test": "321"}]) == [
        {"date": "1.5.2021", "test": "123"}, {"date": "11.10.2012", "test": "321"}
    ]


def test_returning_data_to_the_user():
    assert returning_data_to_the_user([{"date": "1", "description": "2", "from": "3", "to": "4",
                                        "operationAmount": {
                                         "amount": "5", "currency": {"name": "6"}
                                        }}]) == ["1 2\n3 -> 4\n5 6\n"]


def test_open_json():
    assert open_json("package.json") == {"name": "tests", "version": "1.0.0", "dependencies": {}}
