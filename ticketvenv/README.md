# HelpDesk IT — система управления заявками

Веб-приложение на Django для учёта заявок в IT-отдел: пользователь создаёт
заявку, инженер берёт её в работу и закрывает. По событиям отправляются
почтовые уведомления, список заявок можно выгрузить в Excel.

## Стек

- Python 3.12 + Django 5.0
- SQLite (по умолчанию) или PostgreSQL на боевом сервере
- Nginx + Gunicorn (см. каталог `deploy/`)

## Быстрый запуск (для разработки)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # затем отредактировать секреты
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Приложение откроется на http://127.0.0.1:8000/

## Автоматическая установка (чистая Ubuntu Server 22.04)

```bash
sudo bash install.sh
```

Скрипт ставит системные пакеты (python3-venv, nginx), создаёт виртуальное
окружение, ставит зависимости, готовит `.env`, применяет миграции и собирает
статику. После этого нужно только создать суперпользователя и поднять сервис.

## Боевое развёртывание

1. Настроить переменные в `.env` (обязательно `DJANGO_DEBUG=False` и свой
   `DJANGO_SECRET_KEY`).
2. Сертификат HTTPS:
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout /etc/ssl/private/ticket.key -out /etc/ssl/certs/ticket.crt
   ```
3. Скопировать `deploy/nginx.conf` в `/etc/nginx/sites-available/ticket`,
   `deploy/ticket.service` в `/etc/systemd/system/`.
4. `sudo systemctl enable --now ticket` и перезапустить nginx.
5. Открыть в фаерволе только нужные порты:
   ```bash
   sudo ufw allow 22/tcp && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
   sudo ufw enable
   ```

## Настройки окружения

Все секреты вынесены в `.env` (см. `.env.example`): ключ Django, режим отладки,
список разрешённых хостов, параметры SMTP и LDAP. Файл `.env` в репозиторий
не коммитится.

## Резервное копирование

`backup_db.sh` делает дамп БД с датой в имени. В cron:

```
0 2 * * * /path/to/backup_db.sh
```

## Основные возможности

- Регистрация пользователей, роли «пользователь» / «инженер».
- Создание, просмотр, обновление и закрытие заявок.
- Почтовые уведомления при создании заявки и смене её статуса.
- Экспорт списка своих заявок в Excel (кнопка на странице «All Tickets»).
- Логи приложения пишутся в `logs/app.log`.
