from django.test import LiveServerTestCase
from django.test import Client
from django.urls import reverse
from selenium import webdriver
from django.conf import settings
class CookieCreate():
    "Создаёт cookie файл сессии с залогинииым пользователем к странице предастовляющей доступ только авторизованым поользователям"

    def __init__(self, driver, client):
        self.driver = driver
        self.client = client


    def createCookie(self, driver):
        self.client.login(username = Testing_User_Prarmiters["name"], password = Testing_User_Prarmiters["password"])
        cookie = self.client.cookies['sessionid']
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh()


    def createCookieByName(self, url_name):
        self.driver.get("http://127.0.0.1:8000/" + reverse(url_name))
        self.createCookie(self.driver)


    def createCookieByURl(self, url):    
        self.driver.get("http://127.0.0.1:8000/" + url)
        self.createCookie(self.driver)
        

