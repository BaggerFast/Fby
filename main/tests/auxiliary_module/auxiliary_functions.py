"""
содержит вспомогательные функции для тестов
"""
import json
import os

from selenium.webdriver.support.ui import Select

from fby_market.settings import TESTS_VALUES_DIR


def form_values_placeholder(id_list, values_list, driver) -> None:
    """Заполняет объекты формы по предоставленному списку id значениями из списка values"""
    for id, value in zip(id_list, values_list):
        element = driver.find_element_by_id(id)
        if element.tag_name == "select":
            select = Select(element)
            select.select_by_visible_text(value)
        else:
            element.send_keys(value)


def add_id(data: list) -> list:
    """
    добавляет "id_" ко всем элементам списка
    """
    return [f'id_{value}' for value in data]


def tests_data_load(filename):
    """
    десериализует данные из json файла
    """
    with open(os.path.join(TESTS_VALUES_DIR, filename), "r") as data_test_values:
        return json.load(data_test_values)
