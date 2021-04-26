from django.test import TestCase, LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from django.conf import settings
from fby_market.settings import Base_URl
from main.tests.Cookie import CookieCreate
from main.tests.Tests_valeus import Commodity_transactios_test_valeus as CTT_valeus

"""
тесты на операци производимые с товарами
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent=4 > main\tests\fixtures\tmp_data.json
"""


def add_id(data: list):
    return [f'id_{value}' for value in data]


def form_values_placeholder(id_list, valeus):
    """заполняет объекты формы по предоставленному списку id значениями из списка valeus"""

    for id, valeu in izip(id_list, valeus):
        element = self.driver.find_element_by_id(id)
        if element.tag_name ==  "select":
            element = Select(element)
            select.select_by_visible_text(valeu)
        else:
           element.send_keys(valeu)


class testLoadingСommodity(LiveServerTestCase):
    """тест на проверку загрузки товаров"""
    fixtures = ['tmp_data.json']

    def setUp(self):
        self.test_user = Client()
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.Cookiecreater = CookieCreate(self.driver, self.test_user)

    def tearDown(self):
        self.driver.quit()

    def testLoadingСommodity(self):
        """
        переходит на страницу загрузки каталога и обновляет каталог после чего проверят наличие блока каталога в ином
        случае выдаёт исключение
        """
        self.Cookiecreater.createCookieByName("catalogue_list")
        self.driver.get(Base_URl + reverse("catalogue_list"))
        element = self.driver.find_element_by_id("button_loader")
        element.click()
        try:
            self.driver.find_element_by_class_name("table table-hover table-borderless")
        except exceptions.NoSuchElementException:
            return False


class testCreateCommodity(LiveServerTestCase):
    """тесты на проверку создания товара"""
    fixtures = ['tmp_data.json']

    def tearDown(self):
        self.driver.quit()

    def testCreateCommodity(self):
        """переходит на страницу загрузки каталога Заполняет форму значениями проверяет переход на catalogue"""
        self.test_user = Client()
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.Cookiecreater = CookieCreate(self.driver, self.test_user)
        self.Cookiecreater.createCookieByName("create_offer")
        self.driver.get(Base_URl + reverse("create_offer"))
        ID_lst_first = add_id([
            "name", "category", "vendor", "vendorCode", "manufacturer", "description", "url", "barcode", "id_code",
            "ShelfLife-timePeriod", "ShelfLife-timeUnit", "ShelfLife-comment", "LifeTime-timePeriod",
            "LifeTime-timeUnit", "LifeTime-comment", "GuaranteePeriod-timePeriod", "GuaranteePeriod-timeUnit",
            "GuaranteePeriod-comment", "length", "width", "height", "weight", "transportUnitSize", "minShipment",
            "quantumOfSupply", "deliveryDurationDays", "id_boxCount",
                    ])
        ID_list_second = add_id(["id_currencyId", "id_discountBase", "id_value", "id_vat", "id_availability"])
        for TestValeus in TestCreateCommodityValeus:
           with self.setUp():
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[0])
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[1])
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                assert self.driver.dinf_element_by_tag_name("title").text != "Catalogue"
