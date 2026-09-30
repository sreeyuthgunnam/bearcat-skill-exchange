# Bearcat Skill Exchange

Bearcat Skill Exchange

Bearcat Skill Exchange is a campus project for Northwest Missouri State
University students to offer small skills, discover potential exchanges,
and connect by email. The product scope and decisions are documented in
the [project blueprint](docs/blueprint.md).

## Requirements

- Python 3.13
- Django 5.2
- Windows PowerShell for the commands below

## Local setup

Each computer creates its own `.venv` and `.env`. From the repository root:

```powershell
py -3.13 -m venv .venv
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

$secret = & .\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
(Get-Content .env) -replace '^DJANGO_SECRET_KEY=.*$', "DJANGO_SECRET_KEY=$secret" | Set-Content .env
$env:DJANGO_SECRET_KEY = $secret

.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

The secret is generated locally and stored in the ignored `.env`; do not
commit that file. `.env.example` contains the non-secret configuration
template.

SQLite is temporary for this scaffold. PostgreSQL configuration is tracked
in BSS-8. GitLab is the team repository for review and merges; GitHub is a
secondary copy used to transfer commits between computers.
