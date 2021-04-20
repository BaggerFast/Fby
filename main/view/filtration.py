class Filtration:
    def __init__(self, attribute_names, fields_to_filter):
        self.attribute_names = attribute_names
        self.fields_to_filter = fields_to_filter

    def get_filter_types(self, items):
        filter_types = {}
        for field, table_index in self.fields_to_filter.items():
            filter_types[field] = {
                'name': self.attribute_names[table_index],
                'options': set([getattr(item, field) for item in items])
            }
        return filter_types

    def filters_from_request(self, request):
        filters = {}
        for field, _ in self.fields_to_filter.items():
            filters[field] = request.GET.get(field)
        return filters

    @staticmethod
    def filter_items(items, filters):
        filtered_items = []
        for item in items:
            passed = True
            for filter_attr, filter_value in filters.items():
                if filter_value and len(filter_value) != 0:
                    if filter_value != getattr(item, filter_attr):
                        passed = False
                        break
            if passed:
                filtered_items.append(item)
        return filtered_items
