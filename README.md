# fby_market_provider

WEB приложение для поставщиков на Яндекс.Маркет. Размещение по схеме FBY (фулфилмент)

## Quickstart

```bash
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
./manage.py runserver
```