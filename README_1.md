# Homework #8 — MongoDB, Redis, RabbitMQ, Docker

## Project Description
An educational project demonstrating how to work with NoSQL databases, message queues, and asynchronous processing using Docker.

Features:
- Store authors and quotes in MongoDB Atlas
- CLI search by author or tags with partial input support
- Search result caching with Redis
- Asynchronous message processing using RabbitMQ (email + SMS)
- Full Docker containerization of all components

---

## Project Structure
```
GOIT-WEB-HW_10/
├── .vscode/                # VSCode editor settings
├── quotes_site/            # Main Django project
│ ├── config/               # Main project settings (settings, urls, wsgi)
│ ├── data/                 # JSON files with authors and quotes (for import)
│ ├── importer/             # Command for loading data from JSON into the DB
│ ├── media/                # Folder for loading media files (avatars)
│ ├── quotesapp/            # Main application with quotes and authors
│ │ ├── migrations/             # Database migrations
│ │ ├── static/quotesapp/       # Static files (css, images)
│ │ ├── templates/quotesapp/    # HTML templates of the application
│ │ ├── models.py               # Models for quotes, authors, tags
│ │ ├── views.py            # Logic of page display
│ │ ├── forms.py            # Forms for adding quotes and authors
│ │ └── urls.py             # URL routes of the application
│ ├── usersapp/             # Application for working with users
│ │ ├── migrations/             # User migrations
│ │ ├── templates/usersapp/     # Templates for login, registration, profile
│ │ ├── models.py               # User profile model (avatar, etc.)
│ │ ├── views.py            # Views for registration, authorization, profile editing
│ │ ├── forms.py            # Forms for registration and profile editing
│ │ ├── signals.py          # Signals for automatic profile creation
│ │ └── urls.py             # URL routes of the users application
├── manage.py               # Starting and managing a Django project
├── poetry.lock             # Fixed versions of Poetry packages
├── pyproject.toml          # Poetry configuration (dependencies project)
├── README.md               # Project documentation

```

---

## Setup & Run

### Clone the repo and create a `.env` file:
```
MONGO_USER=your_user
MONGO_PASS=your_password
MONGO_DB_NAME=your_name
MONGO_DOMAIN=cluster0.xxxxxx.mongodb.net

REDIS_URL=redis://localhost:6379/0

RABBITMQ_USER=admin
RABBITMQ_PASS=admin
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
```

### Install Poetry and dependencies:
```bash
poetry install
poetry shell
```

### Run all services using Docker:
```bash
docker-compose up --build -d
```

### Load data into MongoDB:
```bash
poetry run python src/load_data.py
```

### Search CLI (Redis cache enabled):
```bash
docker-compose up -d search_cli
```
You can also enter the container manually:
```bash
poetry run python src/search_quotes.py
```

Sample commands:
```
names
name:Albert Einstein
tags
tag:life
tags:life,miracle
exit
```

---

## Queues (RabbitMQ)

### Producer:
```bash
docker-compose up -d producer
```

### Consumer Email:
```bash
docker-compose up -d consumer_email
```

### Consumer SMS:
```bash
docker-compose up -d consumer_sms
```

> RabbitMQ Web UI: `http://localhost:15672`  
> Login and password are set in your `.env` file.

---