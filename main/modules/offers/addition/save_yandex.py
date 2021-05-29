from main.ya_requests import UpdateOfferList, YandexChangePricesList


def push_offer_to_ym(request, offers, sku_list, success_msg):
    """Обработка запроса на обновление или сохранение товара на Яндексе"""
    if not offers:
        return
    update_request = UpdateOfferList(offers=list(offers), request=request)
    update_request.update_offers()
    update_request.messages(sku_list=sku_list, success_message=success_msg)


def push_offer_price_to_ym(request, prices, sku_list, success_msg):
    if not prices:
        return
    changed_prices = YandexChangePricesList(prices=prices, request=request)
    changed_prices.update_prices()
    changed_prices.messages(sku_list=sku_list, success_message=success_msg)
