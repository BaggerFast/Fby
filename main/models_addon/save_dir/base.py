from typing import List


class BasePattern:
    """Базовый класс для сохранения данных из json в database"""
    MODELS = {}

    def __init__(self, json: dict):
        self.json: dict = json
        self.created_objects: List = []
        self.updated_objects: List = []
        self.errors = []

    def save(self, user) -> None:
        """Сохранение данных order из json в БД

        Метод определяется индивидуально в наследных паттернах
        """
        raise NotImplementedError

    @staticmethod
    def get_dict_from_list(list: List) -> dict:
        """Создание словаря вида {Модель: список объектов} из списка объектов"""
        dict = {}
        for obj in list:
            if obj._meta.model in dict:
                dict[obj._meta.model].append(obj)
            else:
                dict[obj._meta.model] = [obj]
        return dict

    def bulk_update(self, updated_dict: dict) -> None:
        """Обновление множества объектов одним запросом на каждую модель"""
        for model, objects in updated_dict.items():
            model.objects.bulk_update(
                objects,
                self.MODELS[model]['update_fields']
            )

    def bulk_create(self, created_dict) -> None:
        """Создание множества объектов одним запросом на каждую модель"""
        for model, objects in created_dict.items():
            model.objects.bulk_create(
                objects,
                ignore_conflicts=True
            )

    def bulk_create_update(self):
        """Создание и обновление множества объектов"""
        created_dict = self.get_dict_from_list(self.created_objects)
        updated_dict = self.get_dict_from_list(self.updated_objects)
        self.bulk_update(updated_dict)
        self.bulk_create(created_dict)
