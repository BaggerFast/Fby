from main.views import *


class CatalogueView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {
            'offers': None
        }

    def get(self, request):
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
