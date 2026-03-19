# Yellow Crumble
### EEN1037 Web Application Development — Assignment 2

Yellow Crumble is a full-stack dessert ordering web application built with **Python Django**, 
containerised using **Docker**, and backed by a **PostgreSQL** database.

---

## Requirements

- Docker Desktop
- Docker Compose

---

## Running the Application

Clone or extract the project folder, then run the following command from the project root:
```bash
docker compose up
```

The application will be available at **http://localhost:8000**

---

## First Run Setup

On the first run, the following happens automatically:

- PostgreSQL database is created
- Django migrations are applied
- Example fixture data is loaded (menu items, categories, careers, etc.)

---

## Default Admin Account

An admin superuser is created automatically on first run:

| Field    | Value |
|----------|-------|
| Username | admin |
| Password | admin |

The Django Admin panel is accessible at **http://localhost:8000/admin**

---

## Database Access

The PostgreSQL database can be accessed directly with a tool such as **DBeaver**:

| Field    | Value      |
|----------|------------|
| Host     | localhost  |
| Port     | 5432       |
| Database | myappdb    |
| Username | myappdbuser|
| Password | myappdbpass|

---

## Project Structure
```
myapp/
├── fixtures/          # Example seed data
├── migrations/        # Django database migrations
├── static/            # CSS and image files
├── templates/         # HTML templates
├── models.py          # Database models
├── views.py           # View functions
├── urls.py            # URL routing
└── forms.py           # Form definitions
```

---

## Pages & Routes

| Page        | URL           |
|-------------|---------------|
| Home        | /             |
| Menu/Order  | /index.html   |
| About Us    | /about.html   |
| Contact     | /contact.html |
| FAQ         | /faq.html     |
| Careers     | /careers.html |
| Gallery     | /gallery.html |
| Reviews     | /reviews.html |
| Newsletter  | /newsletter.html |
| Login       | /login/       |
| Register    | /register/    |
| Profile     | /profile/     |

---

## Stopping the Application

Stop the containers:
```bash
docker compose down
```

Stop the containers and delete the database volume for a completely fresh start:
```bash
docker compose down -v
```