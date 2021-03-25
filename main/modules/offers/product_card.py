from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view import *


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def post(self, request, id):
        current_offer = Offer.objects.get(id=id)
        current_barcode = Barcode.objects.get(offer=current_offer)
        current_url = Url.objects.get(offer=current_offer)
        current_weight = WeightDimension.objects.get(offer=current_offer)

        request_post = request.POST.dict()
        request_post['shopSku'] = current_offer.shopSku
        request_post['marketSku'] = current_offer.marketSku

        disable = True

        self.context['navbar'] = get_navbar(request)
        self.context['disable'] = disable

        offer_f = OfferForm(disable, request_post, instance=current_offer)
        print(offer_f.errors)
        barcode_f = BarcodeForm(disable, request_post, instance=current_barcode)
        url_f = UrlForm(disable, request_post, instance=current_url)
        logistic_f = LogisticForm(disable, request_post, instance=current_offer)
        weight_f = WeightDimensionForm(disable, request_post, instance=current_weight)

        if offer_f.is_valid() and barcode_f.is_valid() and url_f.is_valid() and logistic_f.is_valid() and weight_f.is_valid():
            offer_f.save()
            barcode_f.save()
            url_f.save()
            logistic_f.save()
            weight_f.save()

            self.context['forms'] = {'Основная информация': ['offer_info', [OfferForm(instance=current_offer, disable=disable),
                                                                            UrlForm(instance=current_url, disable=disable),
                                                                            BarcodeForm(instance=current_barcode, disable=disable)]],
                                     'Габариты и вес в упаковке': ['weight_info',
                                                                   [WeightDimensionForm(instance=current_weight, disable=disable)]],
                                     'Особенности логистики': ['logistic_info',
                                                               [LogisticForm(instance=current_offer, disable=disable)]]}
        else:
            messages.error(request, 'Произошла ошибка!')
        return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)

        offer = Offer.objects.get(id=id)
        weight = WeightDimension.objects.get(offer=id)
        url = Url.objects.get(offer=id)
        barcode = Barcode.objects.get(offer=id)
        # timings = Timing.objects.get(offer=id)

        disable = False if int(request.GET.get('edit', 0)) else True

        self.context['disable'] = disable
        self.context['forms'] = {'Основная информация': ['offer_info', [OfferForm(instance=offer, disable=disable),
                                                         UrlForm(instance=url, disable=disable),
                                                         BarcodeForm(instance=barcode, disable=disable)]],
                                'Габариты и вес в упаковке': ['weight_info', [WeightDimensionForm(instance=weight, disable=disable)]],
                                'Особенности логистики': ['logistic_info', [LogisticForm(instance=offer, disable=disable)]]}
        # self.context['timing_form'] = TimingForm(instance=timings)

        return render(request, Page.product_card, self.context)
