"""Базовые классы сериалайзеров

Определяют методы create() и update() для сериалайзеров сложной структуры
для поддержки десериализации
"""

from typing import List
from rest_framework import serializers
from rest_framework.utils import model_meta


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Родительский класс для сериализаторов с вложенной структурой.

    Определяют методы create() и update() и ключевое поле для передачи дочерним объектам
    """

    @staticmethod
    def forward_name() -> str:
        """
        Ключ для передачи экземпляра модели (instance) дочернему объекту

        Определяется индивидуально в наследуемых сериализаторах
        """
        raise NotImplementedError('`forward_name()` must be implemented.')

    def forward_kwargs(self, instance) -> dict:
        """Словарь для передачи экземпляра модели (instance) дочернему объекту """

        return {self.forward_name(): instance}

    def foreign_fields(self) -> List[str]:
        """Список foreign-полей модели (для связи с родителями)"""

        return [field
                for field in self.fields
                if field in model_meta.get_field_info(self.Meta.model).forward_relations]

    def nested_fields(self) -> List[str]:
        """Список вложенных полей сериализатора (за исключением foreign-полей)"""

        return [field
                for field in self.fields
                if isinstance(self.fields[field], serializers.BaseSerializer) and field not in self.foreign_fields()]

    def get_foreign_object(self, field: str, **kwargs: dict):
        """Экземпляр родительского объекта для foreign-поля field в соответствии c **kwargs"""
        foreign_serializer = self.fields[field]
        foreign_model = foreign_serializer.Meta.model
        return foreign_model.objects.get_or_create(**kwargs)[0]

    def nested_validated_data(self, instance, field, data):
        """validated_data для встроенного сериализатора"""
        nested_serializer = self.fields[field]
        if getattr(nested_serializer, 'many', False):
            return [{**attrs, **self.forward_kwargs(instance)} for attrs in data]
        else:
            return {**data, **self.forward_kwargs(instance)}

    def get_nested_object(self, instance, field: str):
        """Возвращает встроенный объект для поля field"""
        return getattr(instance, field, None)

    def create(self, validated_data: dict):
        """Создание нового объекта на основании validated_data"""

        foreign_dict = {field: validated_data.pop(field, None)
                        for field in self.foreign_fields()}
        nested_dict = {field: validated_data.pop(field, None)
                       for field in self.nested_fields()}

        foreign_instances = {field: self.get_foreign_object(field, **foreign_dict[field])
                             for field in self.foreign_fields()}

        instance = self.Meta.model.objects.create(**foreign_instances, **validated_data)

        for field, data in nested_dict.items():
            if data:
                nested_serializer = self.fields[field]
                nested_serializer.create(validated_data=self.nested_validated_data(instance, field, data))

        return instance

    def update(self, instance, validated_data: dict):
        """Обновление объекта instance на основании validated_data"""

        for field in self.foreign_fields():
            foreign_data = validated_data.pop(field, None)
            if foreign_data:
                foreign_instance = self.get_foreign_object(field, **foreign_data)
                setattr(instance, field, foreign_instance)
            else:
                setattr(instance, field, None)

        for field in self.nested_fields():
            nested_serializer = self.fields[field]
            nested_data = validated_data.pop(field, None)
            nested_object = self.get_nested_object(instance, field)
            if nested_data:
                if nested_object:
                    nested_serializer.update(instance=nested_object,
                                             validated_data=self.nested_validated_data(instance, field, nested_data))
                else:
                    nested_serializer.create(validated_data=self.nested_validated_data(instance, field, nested_data))
            else:
                if nested_object:
                    if getattr(nested_serializer, 'many', False):
                        nested_object.all().delete()
                    else:
                        nested_object.delete()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance


class BaseListSerializer(serializers.ListSerializer):
    """Родительский класс для сериализаторов-списков.

    Определяют методы create() и update() и ключевые поля идентификации уникальных объектов
    """

    """список ключевых полей модели, идентифицирующих уникальный объект,
        Определяется индивидуально в наследуемых сериализаторах"""
    key_fields: List[str] = []

    def create(self, validated_data: dict) -> List:
        """Создание новых объектов из списка validated_data"""

        return [self.child.create(item) for item in validated_data]

    def update(self, instance, validated_data: dict) -> List:
        """Обновление списка объектов instance на основании списка validated_data"""

        inst_mapping = {' '.join(str(getattr(inst, key_field)) for key_field in self.key_fields): inst
                        for inst in instance.all()}
        data_mapping = {' '.join(str(item[key_field]) for key_field in self.key_fields): item
                        for item in validated_data}

        """Создание и обновление."""
        instances = []
        for object_key_fields, data in data_mapping.items():
            inst = inst_mapping.get(object_key_fields, None)
            if inst is None:
                instances.append(self.child.create(data))
            else:
                instances.append(self.child.update(inst, data))

        """Удаление."""
        for inst_key_fields, inst in inst_mapping.items():
            if inst_key_fields not in data_mapping:
                inst.delete()

        return instances
