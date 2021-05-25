def get_item_display_name(item, field):
    get_display_name = f"get_{field}_display"
    if hasattr(item, get_display_name):
        return getattr(item, get_display_name)()
    else:
        return None


class Filtration:
    def __init__(self, fields_to_filter):
        self.fields_to_filter = fields_to_filter

    def get_filter_types(self, items):
        filter_types = {}
        for field, name in self.fields_to_filter.items():
            options = set()
            for item in items:
                actual_name = getattr(item, field)
                options.add((get_item_display_name(item, field) or actual_name, actual_name))
                options.remove((None, None))
            options = sorted(options, key=lambda x: x[0])
            options_actual = None
            if options:
                options, options_actual = zip(*options)

            filter_types[field] = {
                'name': name,
                'options': options,
                'options_actual': options_actual,
            }
        return filter_types

    @staticmethod
    def filters_from_request(request, filter_types):
        filters = {}
        for index, (field, filter_type) in enumerate(filter_types.items()):
            str_options = [filter_type['options_actual'][int(option)] for option in request.GET.getlist(str(index), '')]
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
