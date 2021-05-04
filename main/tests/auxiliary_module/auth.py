from django.urls import reverse
from django.test.client import Client
from selenium.webdriver import Chrome
from fby_market.settings import BASE_URL, SELENIUM_USER_AUTH_CREDENTIALS
from main.tests.auxiliary_module.auxiliary_functions import form_values_placeholder


class AuthManager:
    """
    Производит авторизацию и перенаправляет на указанную страницу
    """

    def __init__(self, driver: Chrome, client: Client):
        self.driver: Chrome = driver
        self.client: Client = client

    def authorization(self) -> None:
        id_list = ["id_username", "id_password"]
        values_list = [SELENIUM_USER_AUTH_CREDENTIALS['name'], SELENIUM_USER_AUTH_CREDENTIALS['password']]
        form_values_placeholder(id_list, values_list, self.driver)
        element = self.driver.find_element_by_tag_name("button")
        element.click()

    def authorization_by_name(self, url_name: str) -> None:
        self.driver.get(BASE_URL + reverse(url_name))
        self.authorization()

    def authorization_by_url(self, url: str) -> None:
        self.driver.get(BASE_URL + url)
        self.authorization()
