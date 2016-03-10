Ходит в [яндекс карты](https://maps.yandex.ru/) по ссылке и сохраняет в csv файл первый результат по маршрутам и скриншот.
Можно пользоваться сокращателями ссылок.

##### Установка:

```
virtualenv .env
pip install -r requirements.txt
npm install
```

##### Запуск:
```
. .env/bin/activate
./main.py --help
```

или

```
~/route-stat/.env/bin/python ~/route-stat/main.py --url=... --phantomjs=... --csv_path=./to_home.csv --screen_path=./to_home/
```
