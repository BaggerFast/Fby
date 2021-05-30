import itertools
import re
from typing import List
from main.models_addon.ya_market import Offer


def get_item_display_name(item, field: str):
    get_display_name = f"get_{field}_display"
    if hasattr(item, get_display_name):
        return getattr(item, get_display_name)()
    else:
        return None


def search_algorithm(keywords: str, objects: List[Offer], fields) -> List[Offer]:
    if not len(keywords):
        return objects

    keywords = keywords.lower().strip().split('|')

    # Защита от дурака
    keywords = list(filter(lambda a: a != '', keywords))
    keywords = list(filter(lambda a: a != ' ', keywords))

    keywords = [i.strip() for i in keywords]

    print(keywords)
    search_results = []
    for item, keyword in itertools.product(objects, keywords):
        for field in fields:
            attr_display = str(get_item_display_name(item, field)).lower()
            attr_actual = str(getattr(item, field)).lower()
            if (attr_actual and keyword in attr_display or keyword in attr_actual) and not item in search_results:
                search_results.append(item)
                break
    return search_results
