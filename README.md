# Production-and-Manufacturing-Management-System

A production and manufacturing management system built with Django and Vue.js. Tracks products through production stages, provides real-time updates, and optimizes workflows with data visualization and modern, responsive design.

backeges you need to install:
   pip install django
   pip install  mysql
   pip install mysql-connector or mysql-connector-python(if mysql-connector didn't work)
   pip install djangorestframework
   activite the virtual environment to run it right 
   tesing git add .
   installing pakage pip install django-extensions to be able to lists of the endpoints ..... run this to see our routes python manage.py show_urls
>>after you install the pakage pip install django-extensions 

---

## Running locally (SQLite)

```powershell
# backend
$env:DB_ENGINE = 'sqlite'
$env:DB_NAME  = 'C:\path\to\fpms-demo.sqlite3'
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# frontend (separate terminal)
cd FPMS\client
npm install
npm run dev
```

Demo accounts (after running `seed_demo.py`, password `demo1234`):
`admin@demo.com`, `pm@demo.com`, `planner@demo.com`, `qcm@demo.com`,
`qci@demo.com`, `supervisor@demo.com`, `operator@demo.com`.

## API authentication

* `POST /api/admin/users/login/` → `{ user, access, refresh }`
* Send `Authorization: Bearer <access>` on every API request.
* `POST /token/refresh/` with `{ refresh }` returns a new access token.
* Every endpoint requires authentication. Admin-only endpoints
  (`/users/`, `/departments/`, `/roles/`, `/settings/`, `/backups/`,
  `/activity-logs/`) return `403` for non-admin roles.

## Activity log (audit trail)

Every model change (create/update/delete) and every login is written to
`ActivityLog`. The actor is resolved automatically:

* session user when available,
* otherwise the user encoded in the `Authorization: Bearer <access>` token
  (decoded server-side, because DRF authenticates inside the view).

Each entry also stores the client IP (`X-Forwarded-For`, falling back to
`REMOTE_ADDR`), plus `user_agent`, `request_method` and `request_path` in
`details`. Changes made outside a request (management commands, shell,
data migrations) are still logged with `user = null`.

Admin users can read the trail at `GET /api/admin/activity-logs/`.

## Production orders ↔ work orders

`WorkOrder` has an optional `production_order` FK, so an execution work
order can be traced back to the planning production order:

* `POST /api/work_orders/` accepts `production_order` (nullable).
* `GET /api/work_orders/?production_order=<id>` filters work orders.
* `GET /api/production-orders/<id>/` includes `work_orders` (ids) and
  `work_orders_count`.

## Tests

```powershell
$env:DB_ENGINE = 'sqlite'
$env:DB_NAME  = 'C:\path\to\fpms-test.sqlite3'
python manage.py test
```

## MySQL note

If the `administration_notification` table already exists on a MySQL
database, mark the migration as applied before running `migrate`:

```bash
python manage.py migrate administration 0005 --fake
```

