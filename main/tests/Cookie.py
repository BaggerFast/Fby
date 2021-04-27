from django.urls import reverse
from django.test.client import Client
from selenium.webdriver import Chrome
from fby_market.settings import BASE_URL, SELENIUM_USER_AUTH_CREDENTIALS


class CookieManager:
    """
    Создаёт cookie файл сессии с авторизованным пользователем к странице предоставляющей
    доступ только авторизованным пользователям
    """

    def __init__(self, driver: Chrome, client: Client):
        self.driver: Chrome = driver
        self.client: Client = client

    def create_cookie(self, driver: Chrome) -> None:
        self.client.login(username=SELENIUM_USER_AUTH_CREDENTIALS["name"],
                          password=SELENIUM_USER_AUTH_CREDENTIALS["password"])
        cookie = self.client.cookies['sessionid']
        self.driver.add_cookie(
            {
                'name': 'sessionid',
                'value': cookie.value,
                'secure': False,
                'path': '/'
            }
        )
        self.driver.refresh()

    def set_cookie_by_name(self, url_name: str) -> None:
        self.driver.get(BASE_URL + reverse(url_name))
        self.create_cookie(self.driver)

    def create_cookie_by_url(self, url: str) -> None:
        self.driver.get(BASE_URL + url)
        self.create_cookie(self.driver)
