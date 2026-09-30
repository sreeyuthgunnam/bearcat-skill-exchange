# Bearcat Skill Exchange

Bearcat Skill Exchange

Bearcat Skill Exchange is a campus project for Northwest Missouri State
University students to offer small skills, discover potential exchanges,
and connect by email. The product scope and decisions are documented in
the [project blueprint](docs/blueprint.md).

## Requirements

- Python 3.11 or 3.13
- Django 5.2
- PostgreSQL 18
- Windows PowerShell for the commands below

## Local setup

Each computer uses its own local PostgreSQL 18 database and its own ignored
`.env` file. The local database is named `bearcat_skill_exchange`, owned by
the `bse_app` role, and listens on `localhost:5432`. Create that database and
role on each computer, and set the role's password locally; no database or
password is shared through Git. Existing `.env` files are left untouched by
the setup commands below.

From the repository root in PowerShell. If `.venv` already exists, skip
environment creation; otherwise create it with the Python version you will
use (3.11 or 3.13):

```powershell
python -m venv .venv
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

$env:DJANGO_SECRET_KEY = & .\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

To set up the local role and database, connect to PostgreSQL as a local
administrator using `psql`, then run the applicable commands in its prompt.
If the role already exists, skip `CREATE ROLE`; run `\password bse_app` only
if you need to set or reset its local password. If the database already
exists, skip `CREATE DATABASE`.

```powershell
psql -h localhost -p 5432 -U your_local_admin_role
```

```sql
CREATE ROLE bse_app LOGIN;
\password bse_app
CREATE DATABASE bearcat_skill_exchange OWNER bse_app;
\q
```

Enter the prompted role password into `POSTGRES_PASSWORD` in your local
`.env`; replace the example placeholder before starting Django. The generated
Django secret stays in the current PowerShell session; to keep it across
sessions, add it to `DJANGO_SECRET_KEY` in the ignored `.env`. Keep `.env`
private and do not commit it. Repeat this setup independently on each
computer. GitLab is the team repository for review and merges; GitHub is a
secondary copy used to transfer commits between computers.
