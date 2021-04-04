"""Базовые классы сериалайзеров

Определяют методы create() и update() для сериалайзеров сложной структуры
для поддержки десериализации
"""

from typing import List

from rest_framework import serializers
from rest_framework.utils import model_meta


class BaseModelSerializer(serializers.ModelSerializer):
    """Родительский класс для сериалайзеров с вложенной структурой.

    Определяют методы create() и update() и ключевое поле для передачи дочерним объектам
    """

    @staticmethod
    def forward_name() -> str:
        """Ключ для передачи экземпляра модели (instance) дочернему объекту

        Определяется индивидуально в наследуемых сериализаторах
        """
        raise NotImplementedError('`forward_name()` must be implemented.')

    def forward_kwargs(self, instance):
        """Словарь для передачи экземпляра модели (instance) дочернему объекту """

        return {self.forward_name(): instance}

    def foreign_fields(self) -> List[str]:
        """Список foreign-полей модели (для связи с родителями)"""

        return [field
                for field in self.fields
                if field in model_meta.get_field_info(self.Meta.model).forward_relations]

    def nested_fields(self):
        """Список вложенных полей сериализатора (за исключением foreign-полей)"""

        return [field
                for field in self.fields
                if isinstance(self.fields[field], serializers.BaseSerializer)
                and field not in self.foreign_fields()
                ]

    def get_parent_object(self, field, **kwargs):
        """Экземпляр родительского объекта для foreign-поля field в соответствии c **kwargs"""
        parent_serializer = self.fields[field]
        return parent_serializer.Meta.model.objects.get_or_create(**kwargs)[0]

    def nested_validated_data(self, instance, field, data):
        """validated_data для встроенного сериализатора"""
        nested_serializer = self.fields[field]
        if getattr(nested_serializer, 'many', False):
            return [{**attrs, **self.forward_kwargs(instance)} for attrs in data]
        else:
            return {**data, **self.forward_kwargs(instance)}

    def create(self, validated_data):
        """Создание нового объекта из validated_data"""

        parent_dict: dict = {field: validated_data.pop(field, None)
                             for field in self.foreign_fields()}
        nested_dict: dict = {field: validated_data.pop(field, None)
                             for field in self.nested_fields()}

        parent_instances: dict = {field: self.get_parent_object(field, **parent_dict[field])
                                  for field in self.foreign_fields()}

        instance = self.Meta.model.objects.create(**parent_instances, **validated_data)

        for field, data in nested_dict.items():
            if data is not None:
                nested_serializer = self.fields[field]
                nested_serializer.create(validated_data=self.nested_validated_data(instance, field, data))

        return instance

    def update(self, instance, validated_data):
        """Обновление объекта instance на основании validated_data"""

        for field in self.foreign_fields():
            parent_data = validated_data.pop(field, None)
            if parent_data is not None:
                parent_instance = self.get_parent_object(field, **parent_data)
                setattr(instance, field, parent_instance)
            else:
                setattr(instance, field, None)

        for field in self.nested_fields():
            nested_serializer = self.fields[field]
            nested_data = validated_data.pop(field, None)
            nested_object = getattr(instance, field, None)
            if nested_data is not None:
                if nested_object is not None:
                    nested_serializer.update(instance=nested_object,
                                             validated_data=self.nested_validated_data(instance, field, nested_data))
                else:
                    nested_serializer.create(validated_data=self.nested_validated_data(instance, field, nested_data))
            else:
                if nested_object is not None and not getattr(nested_serializer, 'many', False):
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

    def create(self, validated_data):
        """Создание новых объектов из списка validated_data"""

        return [self.child.create(item) for item in validated_data]

    def update(self, instance, validated_data):
        """Обновление списка объектов instance на основании списка validated_data"""

        inst_mapping: dict = {' '.join(str(getattr(inst, key_field)) for key_field in self.key_fields): inst
                              for inst in instance.all()}
        data_mapping: dict = {' '.join(str(item[key_field]) for key_field in self.key_fields): item
                              for item in validated_data}

        """Создание и обновление."""
        ret = []
        for object_key_fields, data in data_mapping.items():
            inst = inst_mapping.get(object_key_fields, None)
            if inst is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(inst, data))

        """Удаление"""
        for inst_key_fields, inst in inst_mapping.items():
            if inst_key_fields not in data_mapping:
                inst.delete()

        return ret
