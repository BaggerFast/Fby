from django.test import LiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium import webdriver
from django.conf import settings 
from fby_market.settings import Base_URl, Testing_User_Prarmiters


class CookieCreate:
    """
    Создаёт cookie файл сессии с авторизованным пользователем к странице предоставляющей
    доступ только авторизованным пользователям
    """

    def __init__(self, driver, client):
        self.driver = driver
        self.client = client

    def createCookie(self, driver):
        self.client.login(username=Testing_User_Prarmiters["name"], password=Testing_User_Prarmiters["password"])
        cookie = self.client.cookies['sessionid']
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh()

    def createCookieByName(self, url_name):
        self.driver.get(Base_URl + reverse(url_name))
        self.createCookie(self.driver)

    def createCookieByURl(self, url):    
        self.driver.get(Base_URl + url)
        self.createCookie(self.driver)
        

