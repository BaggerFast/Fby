from django.db.models import Sum
from main.models_addon.ya_market import Offer


def calculate_total_cost(orders):
    """
    Подсчитать доход
    :param orders: Заказы для подсчёта
    :return: Общий доход
    """
    get_sum = orders.aggregate(Sum('items__prices__total')).values()
    if None not in get_sum:
        total_cost = round(*get_sum)
    else:
        total_cost = 0
    return total_cost


def calculate_total_net_cost(orders, offers):
    """
    Подсчитать себестоимость
    :param orders: Заказы для подсчёта
    :param offers: Товары
    :return: Общая себестоимость
    """
    get_sum = offers.filter(marketSku__in=orders.values('items__prices__item__marketSku')).\
        select_related('price').aggregate(Sum('price__net_cost')).values()

    if None not in get_sum:
        total_net_cost = round(*get_sum)
    else:
        total_net_cost = 0
    return total_net_cost


def calculate_revenue(income, net_cost):
    """
    Ф-ия для подсчёта выручки. Рассчитывается по простой формуле *income* - *net_cost*
    :param income: Доход
    :param net_cost: Себестоимость
    :return: Выручка
    """
    return round(income - net_cost)


class SecondaryStats:
    """
    Класс второстепенных stats.
    """

    def __init__(self, time='', orders=None, offers=None):
        """
        Инициализация объекта
        :param time: В какое время подсчитывалось время(прошлый, текущий месяц и т.п.). Строка должна отвечать на вопрос
                     **когда?**
        :param orders: Заказы
        """
        if orders is not None:
            self.time = time
            self.amount = orders.count()
            self.total_cost = calculate_total_cost(orders)
            if offers is not None:
                self.total_net_cost = calculate_total_net_cost(orders, offers)
            else:
                self.total_net_cost = 0
            self.revenue = calculate_revenue(float(self.total_cost), float(self.total_net_cost))


class Stat:
    """
    Класс параметра для статистики.
    """

    def __init__(self, name=None, all_orders=None,
                 included_statuses=('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'),
                 request=None):
        """
        Инициализация объекта класса параметр
        :param name: Название параметра
        :param all_orders: Заказы, лист из 2 объектов - заказы за пред. месяц и за тек. месяц соответственно
        :param included_statuses: Какие статусы для фильтра должны быть, если не заданы то берутся стандартные:
            'DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'
        """
        if len(all_orders) == 1:
            all_orders.append(None)
        filtered_orders = []
        for in_orders in all_orders:
            if in_orders is not None:
                filtered_orders.append(in_orders.filter(status__in=included_statuses))
            else:
                filtered_orders.append(None)
        if request:
            offers = Offer.objects.filter(user=request.user)
        else:
            offers = None
        self.secondary_stats = [
            SecondaryStats('в этом месяце', filtered_orders[0], offers),
            SecondaryStats('ранее', filtered_orders[1], offers)
        ]
        self.name = name
