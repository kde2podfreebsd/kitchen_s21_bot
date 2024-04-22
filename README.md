## How to set-up

### Setup .env
```shell
# https://t.me/kitchen_s21_bot
TELEGRAM_BOT_TOKEN=<tg_bot_token>
TELEGRAM_PAYMENT_BOT_TOKEN=<payment_token>

# DATABASE CONFIG
POSTGRES_USER=dev
POSTGRES_PASSWORD=1234
POSTGRES_DB=kitchen
POSTGRES_HOST=db
POSTGRES_PORT=5432

# PGADMIN CONFIG
PGADMIN_DEFAULT_EMAIL=root@root.com
PGADMIN_DEFAULT_PASSWORD=root

# Кол-во записей для отображения на 1ой странице слайдера
FEEDBACK_STRINGS_PER_PAGE=1
TRANSACTION_STRINGS_PER_PAGE=1

# sheet_id достаем из ссылки https://docs.google.com/spreadsheets/d/1LcUtVUIM6aMeOyiaFqqO1xcNiOyTazxYfIf2b44i0pI/edit#gid=0
GOOGLE_SHEET_ID=1LcUtVUIM6aMeOyiaFqqO1xcNiOyTazxYfIf2b44i0pI
# тут просто тыкаем предоставить доступ -> всем у кого есть ссылка
GOOGLE_SHEETS_SHARE_LINK=https://docs.google.com/spreadsheets/d/1LcUtVUIM6aMeOyiaFqqO1xcNiOyTazxYfIf2b44i0pI/edit?usp=sharing
```

#### Так же убедитесь что в корне лежит файл credentials.json от console.cloud.google.com/apis
В моем случае это ```kitchens21-814e00d544e3.json``` лежит на одном уровне с ```requirements.txt``` и ```docker-compose.yaml```
```json
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "-----BEGIN PRIVATE KEY-----123123123-----END PRIVATE KEY-----\n",
  "client_email": "main-cook@kitchens21.iam.gserviceaccount.com",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "",
  "universe_domain": "googleapis.com"
}

```
### Автоматический билд через docker-compose

```shell
❯ docker-compose -f docker-compose.yaml build
[+] Building 1.7s (11/11) FINISHED                                                                     docker:default
 => [app internal] load build definition from Dockerfile                                                         0.0s
 => => transferring dockerfile: 446B                                                                             0.0s
 => [app internal] load .dockerignore                                                                            0.0s
 => => transferring context: 2B                                                                                  0.0s
 => [app internal] load metadata for docker.io/library/python:3.9-slim                                           0.0s
 => [app 1/6] FROM docker.io/library/python:3.9-slim                                                             0.0s
 => [app internal] load build context                                                                            0.2s
 => => transferring context: 519.56kB                                                                            0.1s
 => CACHED [app 2/6] WORKDIR /app                                                                                0.0s
 => CACHED [app 3/6] RUN apt-get update     && apt-get install -y --no-install-recommends gcc libpq-dev     &&   0.0s
 => CACHED [app 4/6] COPY requirements.txt /app/                                                                 0.0s
 => CACHED [app 5/6] RUN pip install --upgrade pip     && pip install -r requirements.txt                        0.0s
 => [app 6/6] COPY . /app/                                                                                       0.5s
 => [app] exporting to image                                                                                     1.0s
 => => exporting layers                                                                                          1.0s
 => => writing image sha256:fdf80ad67226430e5da51d1287a2ccd2677fff3379c1e2d949c21a26c01207f0                     0.0s
 => => naming to docker.io/library/kitchen_s21_bot-app           
```

```shell
❯ docker-compose -f docker-compose.yaml up
[+] Running 3/0
 ✔ Container pgadmin4_container  Created                                                                         0.0s 
 ✔ Container db                  Created                                                                         0.0s 
 ✔ Container my_app              Recreated                                                                       0.0s 
Attaching to db, my_app, pgadmin4_container
```

## Ручной запуск проекта
### Виртуальное окружение
```shell
❯ python -m venv venv
❯ soruce venv/bin/activate
❯ pip install -r requirements.txt
```



```shell
# for bash
export PYTHONPATH=$PYTHONPATH:$(pwd)

# for fish
set -x PYTHONPATH $PYTHONPATH (pwd)
```

### Как делать миграции?
#### Alembic init
```shell
cd database/
❯ rm alembic.ini
❯ rm -rf migrations/
❯ alembic init migrations
```
#### Изменить sqlalchemy.url в alembic.ini
```shell
docker inspect pgdb | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.22.0.2",
                   
```

```ini
sqlalchemy.url = postgresql://dev:1234@172.22.0.2:5432/kitchen
```

#### Изменить target_metadata в migrations/env.py
```python
from database.models import Base
target_metadata = Base.metadata
```

#### Создать миграцию
```shell
❯ alembic revision --autogenerate -m 'init'
```

#### Залить миграцию
```shell
alembic upgrade heads
```

### Запустить проект
```shell
python bot/main.py
```



### Help info

* Тестовые данные карты yookassa: 1111 1111 1111 1026 12/22 000

* [Как создать google api для google sheets](https://www.youtube.com/watch?v=zCEJurLGFRk) -> 1:50 - 5:40
* Для добавления .gs скрипта сортировки листов нажмите в Расширения -> Apps Script![](static/app_src_1.jpg)
* Расположите код из gSheets/gSheets_sorts.gs и разверните с конфигурацией из скрина![](static/app_src_2.jpg)

Вспомогательные команды для работы с docker-compose volumes
```shell
# Остановить все докеры
sudo docker stop $(sudo docker ps -a -q)
# Удалить все докеры
sudo docker rm $(sudo docker ps -a -q)
```