"""
Тесты на операции, производимые с товарами
python manage.py dumpdata \
    --exclude auth.permission \
    --exclude contenttypes --indent=4 > main\tests\fixtures\tmp_data.json
"""
import os
from time import sleep

from chromedriver_py import binary_path
from django.test import LiveServerTestCase, Client
from selenium.webdriver.chrome.options import Options
from django.urls import reverse
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import Select
from fby_market.settings import BASE_URL, HEADLESS
from main.tests.auxiliary_module.auth import AuthManager
from main.tests.Tests_values.Commodity_transactios_test_values import TestCreateCommodityValues as CTT_values
from main.tests.auxiliary_module.auxiliary_functions import form_values_placeholder, add_id


class LoadingСommodityTestCase(LiveServerTestCase):
    """Проверка загрузки товаров"""
    fixtures = ['tmp_data.json']

    def setUp(self):
        self.client = Client()
        options = Options()
        options.headless = HEADLESS
        self.driver = webdriver.Chrome(executable_path=binary_path, options=options)
        self.auth_manager = AuthManager(self.driver, self.client)

    def tearDown(self):
        self.driver.quit()

    def test_loading_commodity(self):
        """
        Переходит на страницу загрузки каталога
        и обновляем каталог после чего проверяем наличие таблицы каталога.
        В ином случае выдаём исключение
        """
        self.auth_manager.authorization_by_name('catalogue_list')
        self.driver.get(BASE_URL + reverse('catalogue_list'))
        element = self.driver.find_element_by_id('button_loader')
        element.click()
        try:
            table_item = self.driver.find_element_by_id("catalogue_table")
        except exceptions.NoSuchElementException:
            table_item = None
        self.assertNotEqual(table_item, None)


class CreateCommodity(LiveServerTestCase):
    """тесты на проверку создания товара"""
    fixtures = ['tmp_data.json']

    def setUp(self):
        self.test_user = Client()
        options = Options()
        options.headless = HEADLESS
        self.driver = webdriver.Chrome(executable_path=binary_path, options=options)
        self.auth_manager = AuthManager(self.driver, self.test_user)
        self.auth_manager.authorization_by_name("create_offer")
        self.driver.get(BASE_URL + reverse("create_offer"))
        self.ID_list_first = add_id([
            "name", "category", "vendor", "vendorCode", "manufacturer", "description", "url", "barcode", "id_code",
            "ShelfLife-timePeriod", "ShelfLife-timeUnit", "ShelfLife-comment", "LifeTime-timePeriod",
            "LifeTime-timeUnit", "LifeTime-comment", "GuaranteePeriod-timePeriod", "GuaranteePeriod-timeUnit",
            "GuaranteePeriod-comment", "length", "width", "height", "weight", "transportUnitSize", "minShipment",
            "quantumOfSupply", "deliveryDurationDays", "id_boxCount",
        ])
        self.ID_list_second = add_id(["currencyId", "discountBase", "value", "vat", "availability"])

    def tearDown(self):
        self.driver.quit()

    def create_commodity_base(self, test_values) -> None:
        """
        базовая часть для TestCreateCommodity, не является тестом
        """
        form_values_placeholder(self.ID_list_first, test_values[0], self.driver)
        button = self.driver.find_element_by_id("button_save")
        button.click()
        form_values_placeholder(self.ID_list_second, test_values[1], self.driver)
        button = self.driver.find_element_by_id("button_save")
        button.click()
        assert self.driver.find_element_by_tag_name("title").text != "Catalogue"

    def test_create_commodity(self):
        """переходит на страницу загрузки каталога Заполняет форму значениями проверяет переход на catalogue"""
        for test_values in CTT_values:
            self.create_commodity_base(test_values)



