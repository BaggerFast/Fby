from django.shortcuts import render
from django.views.generic.base import View
from main.request_yandex import OfferList
from main.views import Page
from main.models.base import Offer


class CatalogueView(View):
    context = {
        'offers': None
    }

    def get(self, request):
        if int(request.GET.get('update_data', 0)):
            data = OfferList()
            data.save()
            print('Update offer_db successful')
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
