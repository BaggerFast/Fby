import json
from django.http import HttpRequest
import requests
from django.contrib import messages


class Requests:
    """
    Базовый класс для получения данных и сохранения в БД
    """

    params: dict = None  # параметры запроса в формате json (для post-запросов)

    errors = {
        206: "Запрос выполнен частично.",
        400: "Запрос невалидный.",
        401: "В запросе не указаны авторизационные данные.",
        403: "Неверны авторизационные данные, указанные в запросе, или запрещен доступ к запрашиваемому ресурсу.",
        404: "Запрашиваемый ресурс не найден.",
        405: "Запрашиваемый метод для указанного ресурса не поддерживается.",
        415: "Запрашиваемый тип контента не поддерживается методом.",
        420: "Превышено ограничение на доступ к ресурсу.",
        500: "Внутренняя ошибка сервера. Попробуйте вызвать метод через некоторое время. При повторении ошибки"
             " обратитесь в службу технической поддержки Маркета.",
        503: "Сервер временно недоступен из-за высокой загрузки. Попробуйте вызвать метод через некоторое время.",
    }

    def __init__(self, json_name: str, base_context_name: str, name: str, request: HttpRequest):
        self.request = request
        main_url = 'https://api.partner.market.yandex.ru/v2/campaigns'
        self.url: str = f'{main_url}/{self.request.user.get_shop_id()}/{json_name}.json'
        self.headers_str: str = f'OAuth oauth_token={self.request.user.get_token()},' \
                                f' oauth_client_id={self.request.user.get_client_id()}'
        self.headers: dict = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.base_context_name: str = base_context_name  # название элемента во входном json, содержащего  данные
        self.name: str = name
        self.json_data: dict = self.get_json()

    def get_json(self) -> dict:
        """Получение данных от YM"""
        json_data = self.get_next_page()
        return self.get_all_pages(json_data=json_data) if "OK" in json_data['status'] else json_data

    def get_next_page(self, next_page_token: str = None) -> dict:
        """
        Формирование запроса и получение очередной страницы данных
        (если next_page_token не задан, вернется первая страница)
        """
        url = f'{self.url}?page_token={next_page_token}' if next_page_token else self.url
        if self.params:  # если есть входные параметры, формируем post-запрос
            data = requests.post(url, headers=self.headers, json=self.params)
        else:
            data = requests.get(url, headers=self.headers)
        return data.json()

    def get_all_pages(self, json_data: dict) -> dict:
        """Получение всех страниц данных"""
        while 'nextPageToken' in json_data['result']['paging']:  # если страница не последняя, читаем следующую
            next_page_token = json_data['result']['paging']['nextPageToken']
            next_json_object = self.get_next_page(next_page_token)
            json_data['result'][self.base_context_name] += next_json_object['result'][self.base_context_name]
            json_data['result']['paging'] = next_json_object['result']['paging']
        return json_data

    def key_error(self) -> str:
        cur_error = int(self.json_data["error"]["code"])
        if cur_error in self.errors:
            return self.errors[cur_error]
        return ''

    def save(self) -> bool:
        """Возвращает True, когда модель успешно сохранилась, иначе False"""
        try:
            self.pattern_save()
            messages.success(self.request, f'Модель {self.name} успешно сохранилась')
            return True
        except KeyError:
            messages.error(self.request, f'{self.key_error()} В модели {self.name}')
            return False

    def pattern_save(self) -> None:
        """Сохранение данных в соответствующую БД, используется при GET запрос"""
        pass

    def save_json_to_file(self, file: str) -> None:
        """Сохранение данных в json-файл"""
        with open(file, "w") as write_file:
            json.dump(self.json_data, write_file, indent=2, ensure_ascii=False)
