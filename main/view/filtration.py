def get_item_display_name(item, field):
    get_display_name = "get_{}_display".format(field)
    if hasattr(item, get_display_name):
        return getattr(item, get_display_name)()
    else:
        return None


class Filtration:
    def __init__(self, fields_to_filter):
        self.fields_to_filter = fields_to_filter

    @staticmethod
    def create_option_tuple(item, field):
        actual_name = getattr(item, field)
        display_name = get_item_display_name(item, field)
        if display_name:
            option_tuple = (display_name, actual_name)
        else:
            option_tuple = (actual_name, None)
        return option_tuple

    def create_options(self, items, field):
        options = set()
        for item in items:
            option_tuple = self.create_option_tuple(item, field)
            if option_tuple[0] is not None:
                options.add(option_tuple)
        options = sorted(options, key=lambda x: x[0])
        if options:
            return zip(*options)
        return options, set()

    def get_filter_types(self, items):
        filter_types = {}
        for field, name in self.fields_to_filter.items():
            options, options_actual = self.create_options(items, field)

            filter_types[field] = {
                'name': name,
                'options': options,
                'options_actual': options_actual,
            }
        return filter_types

    @staticmethod
    def get_option_by_index(filter_type, index_any):
        index_int = int(index_any)
        actual = filter_type['options_actual'][index_int]
        if actual is not None:
            return actual
        return filter_type['options'][index_int]

    def filters_from_request(self, request, filter_types):
        filters = {}
        for index, (field, filter_type) in enumerate(filter_types.items()):
            str_options = [self.get_option_by_index(filter_type, option) for option in
                           request.GET.getlist(str(index), '')]
            filters[field] = str_options
        return filters

    @staticmethod
    def find_used_filters(filters):
        used_filters = 0
        for filter_values in filters.values():
            if filter_values:
                used_filters += 1
        return used_filters

    @staticmethod
    def find_passed_fields(filters, item):
        passed_fields = 0
        for filter_attr, filter_values in filters.items():
            for filter_value in filter_values:
                if filter_value == getattr(item, filter_attr):
                    passed_fields += 1
                    break
        return passed_fields

    def filter_items(self, items, filters):
        filtered_items = []
        for item in items:
            used_filters = self.find_used_filters(filters)
            passed_fields = self.find_passed_fields(filters, item)
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
