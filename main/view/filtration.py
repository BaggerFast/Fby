class Filtration:
    def __init__(self, fields_to_filter, choices={}):
        self.fields_to_filter = fields_to_filter
        self.choices = choices

    def get_filter_types(self, items):
        filter_types = {}
        for field, name in self.fields_to_filter.items():
            options = set()
            for item in items:
                get_display_name = "get_{}_display".format(field)
                if hasattr(item, get_display_name):
                    options.add(getattr(item, get_display_name)())
                else:
                    options.add(getattr(item, field))
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
            if field in self.choices.keys():
                str_options = [choice[0] for choice in
                               self.choices[field].find_choice(str_options)]
            else:
                str_options = [filter_type['options'][int(option)]
                               for option in request.GET.getlist(str(index), '')]
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
