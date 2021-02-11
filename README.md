# fby_market_provider

WEB приложение для поставщиков на Яндекс.Маркет. Размещение по схеме FBY (фулфилмент)

## Детали
Проблема новых площадок заключается в отсутствии достаточного или комфортного функционала для партнеров (поставщиков). 
Для покупателей придумали много интересного и удобного, а поставщики работают с площадкой через XML-файлы 
(статистика, каталог, анализ) 
У Яндекса есть API, на базе которого можно построить огромный внутренний мир с удобными инструментами для поставщиков:
1. Удобная статистика в различных разрезах
2. Гибкое и оперативное ценообразование
3. Управление товарным каталогом 
4. Аналитический блок (предварительный расчет рентабельности, рекомендации к поставкам)

## Quickstart

```bash
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
./manage.py runserver
```

## Read more
- FBY API: [https://yandex.ru/dev/market/partner-marketplace/doc/dg/concepts/about.html](https://yandex.ru/dev/market/partner-marketplace/doc/dg/concepts/about.html)


## Документация
```bash
cd docs
sphinx-build -v -b coverage source/ source/coverage/
mv source/coverage/python.txt source/coverage.rst
rm -rf source/coverage/
make html
```
