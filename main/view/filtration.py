from collections import OrderedDict
from django.db.models import Q


def get_item_display_name(item, field):
    return getattr(item, field), getattr(item, f'get_{field}_display')()


class Filtration:
    def __init__(self, fields_to_filter):
        self.fields_to_filter = fields_to_filter

    def get_filter_types(self, items):
        filter_types = {}
        for name, field in self.fields_to_filter.items():
            if 'enum' not in field:
                filter_types[field] = {
                    'name': name,
                    'options': sorted(set(items.values_list(field, flat=True).distinct())),
                }
            else:
                field = field['enum']
                options_actual = items.values_list(field, flat=True).distinct()
                options = [getattr(item, f'get_{field}_display')() for item in items]

                filter_types[field] = {
                    'name': name,
                    'options': list(OrderedDict.fromkeys(options)),
                    'options_actual': list(OrderedDict.fromkeys(options_actual)),
                }
        return filter_types

    @staticmethod
    def filters_from_request(request, filter_types):
        filters = {}
        for index, (field, filter_type) in enumerate(filter_types.items()):
            type = 'options_actual' if 'options_actual' in filter_type else 'options'
            str_options = [filter_type[type][int(option)] for option in request.GET.getlist(str(index), '')]
            filters[field] = str_options
        return filters

    @staticmethod
    def filter_items(items, filters):
        query_set_or = Q()
        query_set_and = Q()
        for key, data in filters.items():
            for index in data:
                query_set_or = query_set_or | Q(**{key: index})
            query_set_and = query_set_and & query_set_or
            query_set_or = Q()
        return items.filter(query_set_and)

    @staticmethod
    def checked_filters_from_request(request, filter_types):
        checked = []
        for index, field in enumerate(filter_types.values()):
            checked_sub = [False] * len(field.get("options"))
            for checked_option in request.GET.getlist(str(index), ''):
                checked_sub[int(checked_option)] = True
            checked.append(checked_sub)
        return checked
