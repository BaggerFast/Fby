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
from django.urls import reverse
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import Select

from fby_market.settings import BASE_URL, BASE_DIR
from main.tests.Cookie import CookieManager
from main.tests.Tests_valeus import Commodity_transactios_test_valeus as CTT_valeus
from main.tests.Tests_valeus.Commodity_transactios_test_valeus import TestCreateCommodityValues


def add_id(data: list):
    return [f'id_{value}' for value in data]


def form_values_placeholder(id_list, values, driver, select):
    """Заполняет объекты формы по предоставленному списку id значениями из списка values"""
    for id, value in zip(id_list, values):
        element = driver.find_element_by_id(id)
        if element.tag_name == "select":
            element = Select(element)
            select.select_by_visible_text(value)
        else:
            element.send_keys(value)


class LoadingСommodityTestCase(LiveServerTestCase):
    """Проверка загрузки товаров"""
    fixtures = ['tmp_data.json']

    def setUp(self):
        os.environ['PATH'] = str(BASE_DIR / 'third_party') + ':' + os.environ.get('PATH')
        self.client = Client()
        self.driver = webdriver.Chrome(executable_path='chromedriver')
        self.cookie_manager = CookieManager(self.driver, self.client)

    def tearDown(self):
        self.driver.quit()

    def test_loading_commodity(self):
        """
        Переходит на страницу загрузки каталога
        и обновляем каталог после чего проверяем наличие таблицы каталога.
        В ином случае выдаём исключение
        """
        self.cookie_manager.set_cookie_by_name('catalogue_list')
        # TODO: поправить авторизацию (ибо не работает)
        self.driver.get(BASE_URL + reverse('catalogue_list'))
        element = self.driver.find_element_by_id('button_loader')
        element.click()
        try:
            # TODO: переделать на id элемента
            table_item = self.driver.find_element_by_class_name("table table-hover table-borderless")
        except exceptions.NoSuchElementException:
            table_item = None
        self.assertNotEqual(table_item, None)


class testCreateCommodity(LiveServerTestCase):
    """тесты на проверку создания товара"""
    fixtures = ['tmp_data.json']

    def tearDown(self):
        self.driver.quit()

    def testCreateCommodity(self):
        """переходит на страницу загрузки каталога Заполняет форму значениями проверяет переход на catalogue"""
        self.test_user = Client()
        self.driver = webdriver.Chrome(executable_path='chromedriver')
        self.cookie_manager = CookieManager(self.driver, self.test_user)
        self.cookie_manager.set_cookie_by_name("create_offer")
        self.driver.get(BASE_URL + reverse("create_offer"))
        ID_lst_first = add_id([
            "name", "category", "vendor", "vendorCode", "manufacturer", "description", "url", "barcode", "id_code",
            "ShelfLife-timePeriod", "ShelfLife-timeUnit", "ShelfLife-comment", "LifeTime-timePeriod",
            "LifeTime-timeUnit", "LifeTime-comment", "GuaranteePeriod-timePeriod", "GuaranteePeriod-timeUnit",
            "GuaranteePeriod-comment", "length", "width", "height", "weight", "transportUnitSize", "minShipment",
            "quantumOfSupply", "deliveryDurationDays", "id_boxCount",
        ])
        ID_list_second = add_id(["currencyId", "discountBase", "value", "vat", "availability"])
        for TestValeus in TestCreateCommodityValues:
            with self.setUp():
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[0], self.driver, None)
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[1], self.driver, None)
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                assert self.driver.dinf_element_by_tag_name("title").text != "Catalogue"
