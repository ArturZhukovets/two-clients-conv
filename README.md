[![dev pipeline](https://git.nordicwise.com/service/frontend-for-communication-with-client/badges/dev/pipeline.svg?ignore_skipped=true&key_text=dev+pipeline&key_width=100)](https://git.nordicwise.com/service/frontend-for-communication-with-client/-/commits/dev)

# Fronted for communication with client.

## Install deps
All commands should be executed via the Linux terminal. Try not to use the IDE terminal to avoid problems.

Установка необходимых пакетов на Ubuntu 22.04:
```bash
sudo apt -q update -y

sudo apt -q install -y software-properties-common

wget -O- 'https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key' | gpg --dearmor | sudo tee '/etc/apt/keyrings/nodesource.gpg'
echo 'deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main' | sudo tee '/etc/apt/sources.list.d/nodesource.list'

wget -O- 'https://download.docker.com/linux/ubuntu/gpg' | gpg --dearmor | sudo tee '/etc/apt/keyrings/docker.gpg'
echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable' | sudo tee /etc/apt/sources.list.d/docker.list

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt -q update -y
sudo apt -q install -y python3.11 python3.11-dev python3.11-venv nodejs docker-ce

sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" -o '/usr/local/bin/docker-compose'
sudo chmod +x '/usr/local/bin/docker-compose'

sudo docker compose version
docker compose version

node -v
npm -v

/usr/bin/python3.11 --version

curl -sSL 'https://bootstrap.pypa.io/get-pip.py' -o './get-pip.py'
/usr/bin/python3.11 './get-pip.py'
rm './get-pip.py'
/usr/bin/python3.11 -m pip --version

npm install --global yarn
yarn --version

./scripts/reinit_env.sh
```

## Configure

Copy `.env.example` to `.env`

## DataBase

Run db:
```bash
./src/_environment.py
```

Web manage db: open http://localhost:18888/ and add your db to `pqAdmin`.


Alembic manage db:

```bash
./src/_db.py -h
```

## Development

Для режима разработки рекомендуется добавить следующие переменные в окружение перед запуском приложения:
```
"PYTHONDEVMODE": "1",
"PYTHONTRACEMALLOC": "1",
"PYTHONUNBUFFERED": "1"
```

## Create patches

```bash
./scripts/create_patch.py 'module_name'
```

## Docker
Create certificate and public key:
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/private.key -out /etc/ssl/certs/certificate.crt
```

Clear all stopped local containers, images and volumes:
```bash
sudo docker system prune --force --all --volumes
```

Build docker image:
```bash
tag=frontend-for-communication-with-client && sudo DOCKER_BUILDKIT=1 docker build --pull --progress=plain -t ${tag} . 
```

Run test container:
```bash
sudo docker compose up --build
```

Update, build and push docker image single line:
```bash
bash -c 'version=dev && repo_tag=git.nordicwise.com:4999/service/frontend-for-communication-with-client:${version} && sudo DOCKER_BUILDKIT=1 docker build --pull --progress=plain -t ${repo_tag} . && sudo docker push ${repo_tag}'
```

```bash
bash -c 'version=prod && repo_tag=git.nordicwise.com:4999/business/frontend-for-communication-with-client-external:${version} && sudo DOCKER_BUILDKIT=1 docker build --pull --progress=plain -t ${repo_tag} . && sudo docker push ${repo_tag}'
```

## Testing

Запуск всех тестов:
```bash
poe test
```

Запуск только тех тестов которые проверяют файлы измененные относительно последнего комита в репозиторий:
```bash
poe test-change
```

Если надо запустить под дебагом, то тогда выполнять файл `./tests/run_pytests.py`.

Настройки vscode для запуска дебага тестов:
```json
{
    "name": "tests",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/tests/run_pytests.py",
    "env": {
        "PYTEST_ADDOPTS": "--quiet --no-header --no-summary --verbosity=0 -p no:sugar"
    },
    "console": "integratedTerminal",
    "justMyCode": false
}
```

Если планируется написание bdd то рекомендуеться поставить этот плагин для vscode: [Cucumber (Gherkin) Full Support](https://marketplace.visualstudio.com/items?itemName=alexkrechik.cucumberautocomplete)

Для генерации рандомных данных используйте: Faker, factory_boy или mimesis.

Для создания mock объектов рекомендуюется использовать mockito,

Для различного рода проверок рекомендуется использовать fluentcheck.



## Profiling

Установить пакеты нужные системные пакеты:
```bash
sudo apt -q update
sudo apt -q install pyprof2calltree kcachegrind  graphviz
```

Запуск профилирования:
```bash
poe profile [имя_профиля]
```

Просмотр результатов
```bash
poe profile-view [имя_профиля]
```


## Version history
1.5.2
- Возможность удалять пользователя.
- Фикс запуска расчета метрик.

1.5.1
- Правка ошибок локализации.

1.5.0
- Локализация админки.

1.4.0
- Настройка дефолтного языка.
- Настройка логотипа и т.п. брендирование.

1.3.0
- изменены расчет метрик.

1.0.0
- Init
