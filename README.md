# FineArt DRF Project

This is a backend project developed using Django Rest Framework for managing expenses, incomes, and other financial transactions. The project allows users to manage their financial transactions, including bank receipts and view the total of their expenses, incomes, and other financial details.

## Installation

To run this project, you will need Python 3.8+ and pip installed on your system. **Python 3.11 or 3.12** is recommended for the smoothest install. On Python 3.14, some packages (e.g. Pillow, PyYAML) have been relaxed to newer versions in `requirements.txt`; if you still see build errors, create the venv with Python 3.12: `python3.12 -m venv env`.

Clone the repository to your local machine (or use the `FineArt-Backend` folder inside the adart-updated repo):

```bash
git clone https://github.com/hamzamgit/financial-app-backend.git
```

Go to the project directory:

```bash
cd financial-app-backend
```

<!-- If this backend lives inside adart-updated, use: cd FineArt-Backend -->

Create a virtual environment:

```bash
python3 -m venv env
```

Activate the virtual environment:

```bash
source env/bin/activate
```

<!-- On Windows: env\Scripts\activate -->

Install the project requirements:

```bash
pip install -r requirements.txt
```

## Commands (Django)

Run these from the **FineArt-Backend** directory (with venv activated), or use the **yarn** shortcuts from the **repo root** (see main [README.md](../README.md)).

| What | Django (from `FineArt-Backend/`) | From repo root (yarn) |
|------|----------------------------------|------------------------|
| **Seed DB** (migrate + test user + types/categories/payments) | `python manage.py seed_db` | `yarn seed` or `yarn backend:seed` |
| **Run API server** | `python manage.py runserver 0.0.0.0:8000` | `yarn backend:run` |
| **Migrations only** | `python manage.py migrate` | `yarn backend:migrate` |
| **Django shell** | `python manage.py shell` | `yarn backend:shell` |
| **Create superuser** (admin) | `python manage.py createsuperuser` | — (run from backend dir) |

On **Windows**, if `yarn seed` fails (e.g. `python3` not found), run the Django commands from `FineArt-Backend` using `python` instead of `python3`, or set up the venv and use `.\env\Scripts\python manage.py seed_db`.

---

## Running the Project

Before running the project, create the database and optionally seed it with a test user and data.

**Option A — Create DB and seed in one step (recommended for local/dev):**

From **FineArt-Backend** (with venv activated):

```bash
python manage.py seed_db
```

Or from **repo root** (uses `python3` from PATH):

```bash
yarn seed
```

This runs migrations, creates a test user, and seeds types, categories, and payment methods. Use these credentials to log in to the AdArt app:

| Field    | Value              |
|----------|--------------------|
| **Email**    | `dev.adil786@gmail.com` |
| **Password** | `AdArtDemo123!`        |

**Option B — Manual setup:**

```bash
python manage.py migrate
python manage.py createsuperuser   # for Django admin and admin-only APIs
```

**Start the development server:**

From **FineArt-Backend**:

```bash
python manage.py runserver 0.0.0.0:8000
```

Or from **repo root**:

```bash
yarn backend:run
```

This will start the server at http://127.0.0.1:8000/. You can then access the APIs by navigating to http://127.0.0.1:8000/api/

- **API base:** http://127.0.0.1:8000/api/
- **Swagger UI:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

The following APIs are available:

- **register** — Registers a new user
- **login** — Logs in an existing user
- **profile** — Manages the user profile
- **change-password** — Changes the user password
- **send-reset-password-email** — Sends an email to reset the user password
- **reset-password** — Resets the user password
- **type** — Manages payment types
- **category** — Manages payment categories
- **payments** — Manages payments
- **transaction** — Manages transactions
- **total-transaction** — Shows the total of expenses, income, and other transactions

You can access these APIs using the appropriate HTTP methods (GET, POST, PUT, DELETE) and the appropriate endpoints.

### API reference (methods and body)

| Endpoint | Method | Description | Body / Params |
|----------|--------|-------------|----------------|
| **register** | POST | Register user | `email`, `first_name`, `last_name`, `gender`, `phone_number`, `password`, `confirm_password` |
| **login** | POST | Login | `email`, `password` → returns `token` (access/refresh) |
| **profile** | GET | Current user profile | — (auth required) |
| **change-password** | POST | Change password | `previous_password`, `password`, `confirm_password` |
| **send-reset-password-email** | POST | Request OTP for reset | `email` |
| **reset-password** | POST | Reset with OTP | `otp`, `password`, `confirm_password` |
| **type** | GET/POST | List or create types | POST: `add_type` |
| **type** | GET/PUT/DELETE | Single type | `/type/<id>/` |
| **category** | GET/POST | List or create categories | POST: `new_category`, `icons?`, `color?` |
| **category** | GET/PUT/DELETE | Single category | `/category/<id>/` |
| **payments** | GET/POST | List or create payments | POST: `payment_method`, `icons?` |
| **payments** | GET/PUT/DELETE | Single payment | `/payments/<id>/` |
| **transaction** | GET/POST | List or create transactions | POST: `type`, `payment_method`, `description`, `category`, `amount`, `image?`, `frequency?` |
| **transaction** | GET/PUT/DELETE | Single transaction | `/transaction/<id>/` |
| **total-transaction** | POST | Totals by type | `trans_type` (type id) |
| **chart-stats** | GET | Chart data (line + pie) for logged-in user | — (auth required) |

Type, category, and payment CRUD are admin-only (IsAdminUser). Transaction and profile are user-scoped. `chart-stats` returns monthly totals and category breakdown for the app charts. For more details, refer to the code documentation.

## Celery (optional)

If Celery fails to import (e.g. `current_app` on some Python versions), the server still runs; recurring transaction scheduling is disabled until Celery is fixed or upgraded.

## Project structure

- `root/` — Django project (settings, urls).
- `account/` — User, auth, profile, password reset.
- `Transaction/` — Type, Category, Payment, Add_Transaction models and APIs.

## Contributing

This project was developed by Muhammad Shahzad. If you want to contribute to this project, please fork the repository and create a pull request.
