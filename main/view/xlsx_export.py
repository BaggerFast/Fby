import os.path
from typing import List, Any, Dict, Tuple

import pandas as pd
from django.db.models import QuerySet
from datetime import datetime

from fby_market import settings


class XLSXTools:
    """
    Class for writing excels
    """

    class Cursor:
        def __init__(self, row, col):
            self.row = row
            self.col = col

        def __iter__(self):
            yield self.row
            yield self.col

    def __init__(self, path: str, sheet_name: str):
        self.path = path
        self.writer = pd.ExcelWriter(path, engine='xlsxwriter')
        self.cursor = self.Cursor(0, 0)
        self.sheet_name = sheet_name
        self.max_cols_width = {}

    def move_cursor(self, row=0, col=0):
        self.cursor.row += row
        self.cursor.col += col

    @property
    def row(self):
        return self.cursor.row

    @property
    def col(self):
        return self.cursor.col

    def auto_size(self, data_frame: pd.DataFrame):
        """
        Autofits width of columns

        :param data_frame: DataFrame
        """

        worksheet = self.writer.sheets[self.sheet_name]

        for idx, col in enumerate(data_frame):
            idx += self.col

            series = data_frame[col]

            if idx not in self.max_cols_width:
                self.max_cols_width[idx] = 0

            max_len = max((
                self.max_cols_width[idx],
                series.astype(str).map(len).max(),
                len(str(series.name))
            )) + 1

            self.max_cols_width[idx] = max_len - 1

            worksheet.set_column(idx, idx, max_len)

    def write_excel(self, data: List[Any]):
        self.cursor = self.Cursor(0, 0)

        self.writer.write_cells(cells=[], sheet_name=self.sheet_name)

        for val in data:
            if type(val) is str:
                if self.assert_mask(val, "row"):
                    self.cursor.row = self.parser(val, "row")

                elif self.assert_mask(val, "row+"):
                    self.move_cursor(row=self.parser(val, "row+"))

                elif self.assert_mask(val, "col"):
                    self.cursor.col = self.parser(val, "col")

                elif self.assert_mask(val, "col+"):
                    self.move_cursor(col=self.parser(val, "col+"))

                else:
                    self._write_cell(str(val))

            elif type(val) is dict:
                self._write_table(val)

        self.writer.save()

    def _write_table(self, data: Dict[str, Any]):
        df = pd.DataFrame.from_dict(data)

        df.to_excel(self.writer,
                    sheet_name=self.sheet_name,
                    startrow=self.row,
                    startcol=self.col,
                    index=False,
                    merge_cells=False)

        self.auto_size(df)

        self.move_cursor(row=len(df) + 1)

    def _write_cell(self, data: str):
        worksheet = self.writer.sheets[self.sheet_name]

        worksheet.merge_range(*self.cursor, self.row, self.col + 5, data)

        self.move_cursor(row=1)

    @staticmethod
    def assert_mask(string: str, mask: str):
        if string.startswith(mask):
            num = string[len(mask):]
            if num.lstrip("-").isdigit():
                return True
        return False

    @staticmethod
    def parser(string: str, mask: str):
        if string.startswith(mask):
            num = string[len(mask):]
            if num.lstrip("-").isdigit():
                return int(num)
        return None


def write_to_excel(query_set: QuerySet,
                   store_name: str,
                   mode="offer",
                   period: Tuple[datetime, datetime] = None,
                   field_names: List[str] = None,
                   exclude=True) -> None:
    """
    :param query_set: QuerySet

    :param store_name: Title of store

    :param mode: "offer" or "order"

    :param period: Tuple of two datetimes

    :param field_names: List of fields, which NO need to be exported or need to be exported

    :param exclude: Defines mode of filtering field_names
    """

    modes = {
        "offer": {
            "title": "Информация по товарам",
            "sheet": "Отчет по товарам"
        },
        "order": {
            "title": "Информация по заказам",
            "sheet": "Отчет по заказам"
        }
    }

    if not field_names:
        field_names = ["id"]
    else:
        field_names.append("id")

    meta = query_set.model._meta

    field_names_ = {field.name: field.verbose_name for field in meta.fields if (field.name in field_names) != exclude}

    xlsx = XLSXTools(os.path.join(
        settings.BASE_DIR,
        # "reports",
        # store_name,
        f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    ), modes[mode]["sheet"])

    table = {}

    for obj in query_set:
        for name, verbose_name in field_names_.items():
            if verbose_name not in table:
                table[verbose_name] = []

            get_display_name = f"get_{name}_display"

            if hasattr(obj, get_display_name):
                table[verbose_name].append(str(getattr(obj, get_display_name)()))
            else:
                table[verbose_name].append(str(getattr(obj, name)))

    if period is not None:
        period_ = f"{period[0].strftime('%Y.%m.%d')} - {period[1].strftime('%Y.%m.%d')}"
    else:
        period_ = 'Все время'

    data = [
        "row1",
        modes[mode]["title"],
        "row+1",
        f"Магазин: {store_name}",
        "row+1",
        f"Период: {period_}",
        "row+1",
        table
    ]

    xlsx.write_excel(data)
