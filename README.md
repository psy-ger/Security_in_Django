Security in Django — Практична частина

Що реалізовано
- Мінімальний додаток `accounts` з моделлю `User` (`username`, `email`, `password` збережено у хешованому вигляді).
- Форми реєстрації та входу з валідацією та хешуванням паролів (`set_password`/`check_password`).
- Захист від CSRF у шаблонах (`{% csrf_token %}`) і ввімкнений `CsrfViewMiddleware` у налаштуваннях.
- Middleware:
  - `AccessLogMiddleware` — логування неавторизованих спроб доступу до захищених сторінок (наприклад, `/profile`).
  - `ErrorHandlingMiddleware` — перехоплює виключення і рендерить `500.html`; перетворює 404-відповіді на `404.html` і логуює їх.
- Приклади захисту:
  - XSS: шаблони Django автоматично екранізують введені користувачем дані; використовуйте `|escape`, якщо потрібно.
  - SQL injection: `accounts.utils.safe_raw_query` демонструє параметризовані SQL-запити через Django DB API.
  - Clickjacking: у `settings.py` встановлено `X_FRAME_OPTIONS = 'DENY'`.

Додані файли
- `accounts/` — код додатку (models, forms, views, urls, middleware, utils).
- `templates/` — `base`, `register`, `login`, `profile`, сторінки 404/500.

Як запустити локально
1. Створіть віртуальне середовище і встановіть Django (проєкт створено з Django 5.x):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install django
```

2. Зробіть міграції і застосуйте їх:

```bash
python3 manage.py makemigrations accounts
python3 manage.py migrate
```

3. Запустіть дев-сервер:

```bash
python3 manage.py runserver
```

4. Відкрийте `http://127.0.0.1:8000/register/` та `http://127.0.0.1:8000/login/` для тестування.

Поради з безпеки та сканування

- CSRF в Django: Django генерує CSRF-токен (звичайно зберігається в cookie) і перевіряє його при POST/запитах, що змінюють стан, через `CsrfViewMiddleware`. Обов'язково вставляйте `{% csrf_token %}` у форми, які змінюють стан.

- XSS: шаблони Django авто-ескейплять змінні за замовчуванням. Уникайте `mark_safe` для неперевірених даних. Використовуйте `{{ value|escape }}` або спеціальні фільтри (`|escapejs`, `|urlencode`) при потребі.

- SQL injection: ніколи не конкатенуйте SQL-рядки з вхідними даними. Використовуйте параметризовані запити (`cursor.execute(query, params)`); див. `accounts/utils.py`.

- OWASP ZAP / робочий процес (локально):
  1. Запустіть Django-сервер на `127.0.0.1:8000`.
  2. Запустіть OWASP ZAP і налаштуйте браузер на проксі ZAP або використайте функції ZAP для сканування.
  3. Запустіть активне сканування вашого сайту.
  4. Перегляньте попередження та пріоритезуйте виправлення (наприклад, відсутні заголовки безпеки, XSS, CSRF тощо).

Типові виправлення після сканування
- Вимкніть `DEBUG` і зберігайте `SECRET_KEY` у змінних оточення.
- Встановіть `SESSION_COOKIE_SECURE = True` і `CSRF_COOKIE_SECURE = True` при використанні HTTPS.
- Додайте CSP (`Content-Security-Policy`) заголовки за потреби.
- Валідовуйте та санітизируйте вхідні дані; використовуйте ORM або параметризовані запити.

Додаткові рекомендації (опційно)
- Використовуйте WAF / CDN (Cloudflare, AWS CloudFront + WAF) для зменшення ризику DDoS.
- Впровадьте rate-limiting (nginx, gunicorn або middleware `django-ratelimit`) для захисту від brute-force.
- Для кращого управління сесіями використовуйте підписані cookie, встановіть `SESSION_COOKIE_HTTPONLY = True`, розгляньте ротацію ключів сесій.
- Застосуйте статичний аналіз коду (Bandit для безпеки, flake8 для стилю).

Чим я можу допомогти далі
- Запустити міграції і підняти дев-сервер у цьому середовищі (потрібен дозвіл на виконання команд).
- Додати автоматизовані тести для реєстрації/входу.
- Додати CSP заголовки і production-ready налаштування безпеки.

