def serialize(page_path: str) -> str:
    return f'pages/{page_path}.html'


class Page:
    """
    Для простого взаимодействия с путями файлов html
    """
    index = serialize('index')
    registration = serialize('profile/registration')
    login = serialize('profile/login')
    catalogue = serialize('offer/catalogue')
    product_card = serialize('offer/product_card')
    order = serialize('order/orders')
    order_page = serialize('order/order_page')
    profile = serialize('profile/profile')
    profile_edit = serialize('profile/profile_edit')
    summary = serialize('analytics/summary')
    faq = serialize('faq')
