class Filtration:
    def __init__(self, fields_to_filter, choices={}):
        self.fields_to_filter = fields_to_filter
        self.choices = choices

    @staticmethod
    def find_choice(choices_class, description):
        """
        Найти нужный пункт и возратить его. Если не найдёт, то возращается лист со строкой 'Active'
        :param choices_class: Класс choices'а.
        :param description: Русское описание пункта(-ов).
        :return: Лист из пунктов.
        """
        choices = []
        for choice in choices_class.choices:
            if choice[1] in description:
                choices.append(choice)

        if choices:
            return choices
        else:
            return [('ACTIVE', 'Поставки будут')]

    @staticmethod
    def get_display_name(item, field):
        get_display_name = "get_{}_display".format(field)
        if hasattr(item, get_display_name):
            return getattr(item, get_display_name)()
        else:
            return getattr(item, field)

    def get_filter_types(self, items):
        filter_types = {}
        for field, name in self.fields_to_filter.items():
            options = set()
            for item in items:
                options.add(self.get_display_name(item, field))
            if None in options:
                options.remove(None)
            options = sorted(options)

            filter_types[field] = {
                'name': name,
                'options': options,
            }
        return filter_types

    def filters_from_request(self, request, filter_types):
        filters = {}
        for index, (field, filter_type) in enumerate(filter_types.items()):
            str_options = [filter_type['options'][int(option)] for option in request.GET.getlist(str(index), '')]
            if field in self.choices.keys():
                str_options = [choice[0] for choice in self.find_choice(self.choices[field], str_options)]
            filters[field] = str_options
        return filters

    def filter_items(self, items, filters):
        filtered_items = []
        for item in items:
            used_filters = 0
            for filter_values in filters.values():
                if filter_values:
                    used_filters += 1

            passed_fields = 0
            for filter_field, filter_values in filters.items():
                for filter_value in filter_values:
                    if filter_value == self.get_display_name(item, filter_field):
                        passed_fields += 1
                        break

            if passed_fields == used_filters:
                filtered_items.append(item)
        return filtered_items
