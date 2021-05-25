from collections import OrderedDict


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
        filtered_items = []
        for item in items:
            used_filters = 0
            for filter_values in filters.values():
                if filter_values:
                    used_filters += 1

            passed_fields = 0
            for filter_attr, filter_values in filters.items():
                for filter_value in filter_values:
                    if filter_value == getattr(item, filter_attr):
                        passed_fields += 1
                        break

            if passed_fields == used_filters:
                filtered_items.append(item)
        return filtered_items

    @staticmethod
    def checked_filters_from_request(request, filter_types):
        checked = []
        for index, field in enumerate(filter_types.values()):
            checked_sub = [False] * len(field.get("options"))
            for checked_option in request.GET.getlist(str(index), ''):
                checked_sub[int(checked_option)] = True
            checked.append(checked_sub)
        return checked
