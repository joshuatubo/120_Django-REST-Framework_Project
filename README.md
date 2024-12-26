# Secure Message Exchange System

This project consists of two Django REST Framework applications that communicate securely through encrypted messages.

## Setup Instructions

1. Create two virtual environments:

```bash
python -m venv sender_env
python -m venv receiver_env
```

2. Activate the virtual environments:

```bash
# For sender app
sender_env\Scripts\activate
# For receiver app
receiver_env\Scripts\activate
```

3. Install dependencies in both environments:

```bash
pip install -r requirements.txt
```

4. Run migrations for both applications:

```bash
python manage.py migrate
```

5. Create superuser for both applications:

```bash
python manage.py createsuperuser
```

6. Run the applications (use different terminals):

```bash
# Sender app (port 8000)
python manage.py runserver

# Receiver app (port 8001)
python manage.py runserver 8001
```

## Features

- Secure user authentication
- Encrypted message transmission
- Custom middleware for security
- User-friendly dashboard
- Message history tracking
