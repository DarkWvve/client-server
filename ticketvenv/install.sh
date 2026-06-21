#!/usr/bin/env bash

# Разворачивает приложение на чистой Ubuntu Server 22.04.
# Запускать с правами sudo:  sudo bash install.sh

set -e

echo "==> Обновление списка пакетов"
sudo apt update

echo "==> Установка системного ПО (Python, venv, nginx)"

if ! command -v python3 &>/dev/null; then
  sudo apt install -y python3
fi
sudo apt install -y python3-venv python3-pip

if ! command -v nginx &>/dev/null; then
  echo "==> Устанавливаю nginx"
  sudo apt install -y nginx
else
  echo "==> nginx уже установлен"
fi

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "==> Создание виртуального окружения"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

echo "==> Установка зависимостей Python"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Подготовка .env"
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "    Создан .env из шаблона. ОБЯЗАТЕЛЬНО отредактируйте secret!"
fi

mkdir -p logs

echo "==> Применение миграций"
python manage.py migrate

echo "==> Сбор статики"
python manage.py collectstatic --noinput || true

echo ""
echo "Установка завершена."
echo "Создайте администратора:   python manage.py createsuperuser"
echo "Запуск (dev):              python manage.py runserver"
echo "запуск:                    gunicorn ticket_system.wsgi (см. deploy/)"
