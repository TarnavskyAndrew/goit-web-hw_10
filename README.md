# Homework #10 — Django Quotes Project

## Project Description

An educational Django project that allows users to:
- Register and log in
- Add quotes and authors
- Tag quotes and filter by tags
- Upload and edit avatar (user profile photo)
- See the Top 10 most used tags dynamically

---

## Features

- Quotes, authors, and tags managed via Django models
- Top 10 tags ranked dynamically based on usage
- Pagination for browsing quotes
- Default and custom avatars for user profiles
- Protected routes with @login_required
- Beautiful responsive interface (custom CSS)
- Data import from JSON using Django custom command

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

### 0. Clone the project
```bash
git clone <your_repo_url>
cd GOIT-WEB-HW_10
```

### 1. Start PostgreSQL container
```bash
docker run --name noteapp-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```

### 2. Install dependencies (via Poetry)
```bash
poetry install
poetry shell
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 5. Load authors and quotes
```bash
python manage.py load_quotes
```

### 6. Run development server
```bash
python manage.py runserver
```
Open `http://localhost:8000` in your browser.

---

## User Features

- **Registration / Login** — Create account and sign in.
- **Add Quote** — Add a quote, select author and tags.
- **Add Author** — Add author with birth date and location.
- **Profile Editing** — Upload or change avatar.
- **Top Tags** — View Top 10 most used tags.

---

## Data Import Command

```bash
python manage.py load_quotes
```
Loads data from:
- `quotes_site/data/quotes.json`
- `quotes_site/data/authors.json`

---

## Avatar Support

- Default avatar if none uploaded
- Custom avatars stored in `media/avatars/`
- Automatically created profile with avatar field

---

## Notes

- All visitors can view quotes and authors.
- Adding content or editing profile requires login.
- Beautiful layout and buttons with consistent styling.

---
