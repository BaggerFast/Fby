def serialize(page: str) -> str:
    return f'pages/{page}.html'


class Page:
    """
    Для простого взаимодействия с путями файлов html
    """
    index = serialize('index')
    registration = serialize('registration')
    login = serialize('login')
    catalogue = serialize('offer/catalogue')
    create_offer = product_card = serialize('offer/product_card')



