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
#python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent=4 > main\tests\fixtures\tmp_data.json
'''тесты на операци производимые с товарами'''

def form_values_placeholder(id_list, valeus):
    '''заполняет объекты формы по предоставленному списку id значениями из списка valeus'''

    for id, valeu in izip(id_list, valeus):
        element = self.driver.find_element_by_id(id)
        if element.tag_name ==  "select":
            element = Select(element)
            select.select_by_visible_text(valeu)
        else:
           element.send_keys(valeu)

class testLoadingСommodity(LiveServerTestCase):
    '''тест на проверку загрузки товаров'''
    fixtures = ['tmp_data.json']

    def setUp(self):
        self.test_user = Client()
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.Cookiecreater = CookieCreate(self.driver, self.test_user)

    def tearDown(self):
        self.driver.quit()


    def testLoadingСommodity(self):
        '''перходит на страницу загрузки каталога и обновляет каталог после чего проверят наличие блока каталога в ином случае выдаёт исключение'''
        self.Cookiecreater.createCookieByName("catalogue_list")
        self.driver.get("http://127.0.0.1:8000/" + reverse("catalogue_list"))
        element = self.driver.find_element_by_id("button_loader")
        element.click()
        try:
            self.driver.find_element_by_class_name("table table-hover table-borderless")
        except exceptions.NoSuchElementException:
            return False

class testCreateCommodity(LiveServerTestCase):
    '''тесты на проверку создания товара'''
    fixtures = ['tmp_data.json']

    def tearDown(self):
        self.driver.quit()
   

    def testCreateCommodity(self):
        '''перходит на страницу загрузки каталога Заполняет форму значениями проверяет переход на catalogue'''
        self.test_user = Client()
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.Cookiecreater = CookieCreate(self.driver, self.test_user)
        self.Cookiecreater.createCookieByName("create_offer")
        self.driver.get("http://127.0.0.1:8000/" + reverse("create_offer"))
        ID_lst_first = [
            "id_name", "id_category", "id_vendor", "id_vendorCode", "id_manufacturer", "id_description", "id_url", "id_barcode", "id_code",
            "id_ShelfLife-timePeriod", "id_ShelfLife-timeUnit", "id_ShelfLife-comment", "id_LifeTime-timePeriod", "id_LifeTime-timeUnit", "id_LifeTime-comment", 
            "id_GuaranteePeriod-timePeriod", "id_GuaranteePeriod-timeUnit", "id_GuaranteePeriod-comment", "id_length", " id_width", "id_height", "id_weight",
            "id_transportUnitSize", "id_minShipment", "id_quantumOfSupply", "id_deliveryDurationDays", "id_boxCount",
                    ]
        ID_list_second = [
            "id_currencyId", "id_discountBase", "id_value", "id_vat", "id_availability",
                            ]
        for TestValeus in TestCreateCommodityValeus:
           with self.setUp():
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[0])
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                form_values_placeholder(ID_list_second, CTT_valeus.TestValeus[1])
                button = self.driver.dinf_element_by_id("button_save")
                button.click()
                assert self.driver.dinf_element_by_tag_name("title").text != "Catalogue"
