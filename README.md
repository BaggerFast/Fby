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

Если у вас Ubuntu 18.04 (виртуалка или старая система), то нужно установить python3.8

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
python3.8 --version
```

После этого устанавливаем зависимости в Virtualenv
```bash
pip install --upgrade pip
pip install -r requirements.txt
mkdir third_party
cd third_party
wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip
unzip chromedriver_linux64
rm chromedriver_linux64
# После этого добавьте папку third_party в $PATH
./manage.py migrate
./manage.py createvasya
./manage.py runserver
```

# Тесты

```bash
# Перед запуском тестов установите Google Chrome (нужен для selenium'а)!
./manage.py test
```

## Read more

- FBY
  API: [https://yandex.ru/dev/market/partner-marketplace/doc/dg/concepts/about.html](https://yandex.ru/dev/market/partner-marketplace/doc/dg/concepts/about.html)

## Документация

```bash
cd docs
sphinx-build -v -b coverage source/ source/coverage/
mv source/coverage/python.txt source/coverage.rst
rm -rf source/coverage/
make html
```


## Codestyle
```bash
DJANGO_SETTINGS_MODULE=fby_market.settings pylint fby_market main manage.py
pycodestyle --ignore=E501 fby_market main manage.py
```
