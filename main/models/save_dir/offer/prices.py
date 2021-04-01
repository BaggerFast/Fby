from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer as OfferModel, Price
from main.models.save_dir.offer.offer import OfferPattern, Base


class Prices:
    class Price(Base):
        def save(self) -> None:
            Price.objects.update_or_create(
                offer=self.offer,
                defaults={
                    "value": self.exist("value"),
                    "vat": self.exist('vat'),
                    "discountBase": self.exist('discountBase')
                }
            )


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

    def save(self, user) -> None:
        """Сохраняет данные в БД"""
        for item in self.json:
            try:
                offer = OfferModel.objects.get(shopSku=item.get('id'), user=user)
            except ObjectDoesNotExist:
                continue
            self.parse_attrs(json=item, attr=offer, diff_class=Prices)
            offer.save()
