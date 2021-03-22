from main.models import Offer as OfferModel
from main.models.save_dir.offer import OfferPattern


class PricePattern(OfferPattern):
    """Класс сохраняющий данные price из json в БД."""

    attrs = {
        'simple': [
            'marketSku',
            'updatedAt',
        ],
        'diff': [
            "price"
        ]
    }

    def save(self) -> None:
        """Сохраняет данные в БД"""
        for item in self.json:
            try:
                offer = OfferModel.objects.get(shopSku=item.get('id'))
            except OfferModel.DoesNotExist:
                continue
            self.parse_attrs(item, offer)
            offer.save()
