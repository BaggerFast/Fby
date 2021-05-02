
def serialize(page_path: str) -> str:
    return f'pages/{page_path}.html'


class Page:
    """
    Для простого взаимодействия с путями файлов html
    """

    index = serialize('index')
    registration = serialize('registration')
    login = serialize('login')
    catalogue = serialize('offer/catalogue')
    create_offer = product_card = serialize('offer/product_card')
    order = serialize('order/orders')
    order_page = serialize('order/order_page')
    profile = serialize('profile')
    profile_edit = serialize('profile_edit')
