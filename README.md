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

## Running the Project

Before running the project, make sure to apply the migrations:

```bash
python manage.py migrate
```

Create a superuser (required for Django admin and for admin-only APIs: type, category, payments):

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

<!-- To allow the mobile app or other devices on the network to reach the API, use: python manage.py runserver 0.0.0.0:8000 -->

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

Type, category, and payment CRUD are admin-only (IsAdminUser). Transaction and profile are user-scoped. For more details, refer to the code documentation.

## Celery (optional)

If Celery fails to import (e.g. `current_app` on some Python versions), the server still runs; recurring transaction scheduling is disabled until Celery is fixed or upgraded.

## Project structure

- `root/` — Django project (settings, urls).
- `account/` — User, auth, profile, password reset.
- `Transaction/` — Type, Category, Payment, Add_Transaction models and APIs.

## Contributing

This project was developed by Muhammad Shahzad. If you want to contribute to this project, please fork the repository and create a pull request.
