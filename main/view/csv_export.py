import csv
import io
from typing import List
from django.db.models import QuerySet


def export_qs_to_csv(query_set: QuerySet, field_names: List[str] = None, exclude=True) -> None:
    """
    :param query_set: QuerySet

    :param field_names: List of fields, which NO need to be exported or need to be exported

    :param exclude: Defines mode of filtering field_names
    """
    if not field_names:
        field_names = ["id"]

    meta = query_set.model._meta

    field_names_ = {field.name: field.verbose_name for field in meta.fields if (field.name in field_names) != exclude}

    with io.open(f"{meta}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(field_names_.values())

        for obj in query_set:
            writer.writerow([getattr(obj, field) for field in field_names_.keys()])
