# FineArt-Backend — Documentation

Django REST API for the AdArt (FinArt) mobile app: authentication, profile, transaction types/categories/payments, and transactions.

---

## 1. Project structure

```
FineArt-Backend/
├── root/                 # Project settings & URL routing
│   ├── urls.py           # API routes (api/...)
│   ├── settings.py
│   └── ...
├── account/              # User auth & profile
│   ├── models.py         # User model (email, first_name, last_name, gender, phone_number, otp)
│   ├── views.py          # Register, Login, Profile, ChangePassword, Reset (send OTP, reset with OTP)
│   ├── serializers.py
│   └── management/commands/
│       └── seed_db.py     # Migrate + seed types/categories/payments + test user
├── Transaction/          # Types, categories, payments, transactions
│   ├── models.py         # Type, Category, Payment, Add_Transaction
│   ├── views.py          # Type/Category/Payment/Transaction ViewSets, total-transaction, chart-stats
│   ├── serializers.py
│   ├── filters.py        # Transaction filters
│   └── pagination.py     # LimitOffsetPagination for transaction list
└── requirements.txt
```

---

## 2. How to run

From repo root (adart-updated):

```bash
cd FineArt-Backend
python3 -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py seed_db  # Migrate + seed data + test user (dev.adil786@gmail.com / AdArtDemo123!)
python manage.py runserver 0.0.0.0:8000
```

- Base URL: **http://127.0.0.1:8000**
- API base: **http://127.0.0.1:8000/api/**

See parent **RUNNING.md** for full steps and Android/iOS URL tips.

---

## 3. API endpoints (flow & usage)

All under `http://127.0.0.1:8000/api/`. Auth uses **JWT**: send `Authorization: Bearer <access_token>` for protected endpoints.

### 3.1 Auth (no token)

| Method | Endpoint | Description | Request body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `register/` | Sign up | `email`, `first_name`, `last_name`, `gender`, `phone_number`, `password`, `confirm_password` | `{ "token": { "access", "refresh" }, "msg" }` |
| POST | `login/` | Log in | `email`, `password` | `{ "token": { "access", "refresh" }, "msg" }` |
| POST | `send-reset-password-email/` | Request OTP | `email` | `{ "msg" }` |
| POST | `reset-password/` | Reset with OTP | `otp`, `password`, `confirm_password` | `{ "msg" }` |

### 3.2 Token refresh (no auth header)

| Method | Endpoint | Description | Request body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `token/refresh/` | New access token | `refresh` (JWT refresh token) | `{ "access" }` |

### 3.3 Authenticated (Bearer token required)

| Method | Endpoint | Description | Request / Response |
|--------|----------|-------------|---------------------|
| GET | `profile/` | Current user | Response: `{ "id", "email", "first_name", "last_name", "gender", "phone_number" }` |
| POST | `change-password/` | Change password | Body: `previous_password`, `password`, `confirm_password`. Response: `{ "msg" }` |

### 3.4 Type / Category / Payment

- **List (any authenticated user):** GET `type/`, GET `category/`, GET `payments/` → array of objects (or paginated if configured).
- **Create/Update/Delete:** **Admin only** (staff user).  
  - Type: POST `type/` body `{ "add_type" }`, PUT `type/<id>/`, DELETE `type/<id>/`.  
  - Category: POST `category/` body `{ "new_category", "color?" }`, PUT `category/<id>/`, DELETE `category/<id>/`.  
  - Payment: POST `payments/` body `{ "payment_method" }`, PUT `payments/<id>/`, DELETE `payments/<id>/`.

### 3.5 Transactions

| Method | Endpoint | Description | Request / Response |
|--------|----------|-------------|---------------------|
| GET | `transaction/` | List (filtered by user; staff sees all). Query: `search`, filters | Paginated: `{ "count", "next", "previous", "results": [ { "id", "type", "type_name", "category", "category_name", "payment_method", "payment_method_name", "description", "amount", "image", "frequency" }, ... ] }` |
| POST | `transaction/` | Create | Body: `type`, `category`, `payment_method`, `description`, `amount`, `frequency` (optional `image`) |
| PUT | `transaction/<id>/` | Update | Same body as create (partial OK) |
| DELETE | `transaction/<id>/` | Delete | 204 |

### 3.6 Totals & charts

| Method | Endpoint | Description | Request / Response |
|--------|----------|-------------|---------------------|
| POST | `total-transaction/` | Sum by type | Body: `{ "trans_type": <type_id> }`. Response: `{ "data": { "amount__sum": <number> }, "type_name": "<name>" }` |
| GET | `chart-stats/` | For charts | Response: `{ "line": { "labels": [...], "datasets": [{ "data": [...] }] }, "pie": [{ "name", "population", "color", "legendFontColor", "legendFontSize" }] }` |

---

## 4. Data flow (high level)

1. **App** sends POST to `login/` or `register/` → receives `token.access` (and `token.refresh`).
2. **App** stores tokens and sends `Authorization: Bearer <access>` on every request.
3. On **401**, app can POST to `token/refresh/` with `refresh` to get a new `access` and retry.
4. **Types/Categories/Payments** are loaded with GET (list); create/update/delete are admin-only.
5. **Transactions** are created/listed/updated/deleted per user; **total-transaction** and **chart-stats** are scoped to the current user.

---

## 5. Seed data & test user

- `python manage.py seed_db`: runs migrations, creates default Type/Category/Payment rows, and a test user.
- **Test login:** Email `dev.adil786@gmail.com`, Password `AdArtDemo123!`

---

## 6. Permissions summary

| Resource | List/Retrieve | Create/Update/Delete |
|----------|----------------|----------------------|
| Register, Login, Reset | AllowAny | — |
| Profile, Change password | IsAuthenticated | — |
| Type, Category, Payment | IsAuthenticated | IsAdminUser |
| Transaction | IsAuthenticated (own or all if staff) | IsAuthenticated (own or staff) |
| total-transaction, chart-stats | — | GET/POST IsAuthenticated |
