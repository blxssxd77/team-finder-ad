git initвариант 1: избранное и фильтрация пользователей.

## Быстрый запуск для ревьюера (Docker)

1. Скопируйте `.env_example` в `.env` (если файла `.env` ещё нет):
   ```bash
   cp .env_example .env
   ```
   Windows (PowerShell): `copy .env_example .env`
2. Убедитесь, что в `.env` указано `TASK_VERSION=1`.
3. Запустите проект:
   ```bash
   docker compose up --build
   ```
4. Откройте http://localhost:8000

При первом запуске автоматически выполняются миграции, сбор статики и загрузка тестовых данных.

### Тестовые аккаунты

| Email | Пароль |
|-------|--------|
| admin@teamfinder.ru | admin12345 |
| maria@example.com | testpass123 |
| nikita@example.com | testpass123 |
| alex@example.com | testpass123 |

## Локальная проверка


```powershell
cd путь\к\team-finder-ad-main-3

py -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

$env:USE_SQLITE="True"
python manage.py migrate
python manage.py load_demo_data
python manage.py runserver
```