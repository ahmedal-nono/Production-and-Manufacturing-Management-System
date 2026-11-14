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

## Cache, background jobs, CDN and RUM

### Cache

* `CACHES` uses `LocMemCache` by default, so the app runs with no extra
  services. Set `REDIS_URL` (e.g. `redis://127.0.0.1:6379/1`) to switch to
  Redis automatically.
* `CACHE_TTL` (seconds, default `60`) bounds how long report aggregates are
  served from cache.
* Report caches are dropped immediately by `post_save`/`post_delete` on
  `ProductionLine`, `ProductionOrder`, `Workflow` and `Stage`, so a write is
  never masked by a stale entry.

### Background jobs

Slow work (database backups, scheduled tasks) is queued in
`administration_backgroundjob` instead of blocking the request:

* `POST /api/admin/backups/enqueue_backup/` returns `202 Accepted` with the
  job (`id`, `status`).
* `GET /api/admin/jobs/<id>/` returns the same job, including `result` or
  `error` once it finishes.
* Run the worker next to the web process:

```powershell
python manage.py run_worker              # poll forever
python manage.py run_worker --once       # drain the queue and exit (cron)
```

* `BACKGROUND_JOBS_EAGER=1` executes jobs inline as soon as they are queued
  (useful for demos and tests without a worker).
* `python manage.py run_scheduled_backups` now only queues the due backups;
  the worker performs them.

**Reliability**

* Failed jobs are retried with exponential backoff (2 s, 4 s, 8 s … capped at
  five minutes) until `BACKGROUND_JOBS_MAX_ATTEMPTS` runs (default `3`).
  `GET /api/admin/jobs/<id>/` exposes `attempts`, `max_attempts`,
  `available_at` and `error`.
* A job left `running` by a crashed worker is recovered automatically:
  `run_worker` re-queues it when `BACKGROUND_JOBS_STALE_AFTER` seconds pass
  (default `900`), or marks it failed once attempts are exhausted.
  Use `run_worker --stale-after 300` / `--no-recover` to tune this per run.
* `python manage.py prune_jobs --days 30` deletes old finished jobs
  (`BACKGROUND_JOBS_RETENTION_DAYS`, default `30`).

### Measuring report performance

`manage.py benchmark_reports` runs every report endpoint with a cold and a warm
cache and prints the median latency of each:

```powershell
python manage.py benchmark_reports --runs 5
python manage.py benchmark_reports --runs 10 --json benchmark.json
```

### Static files and CDN

* `STATIC_URL` can be overridden with an environment variable, e.g.
  `STATIC_URL=https://cdn.example.com/static/`.
* WhiteNoise ships in `requirements.txt` and serves collected files straight
  from the WSGI process (with gzip/Brotli), so `/static/` works with
  `DEBUG=False` without a separate web server:

```powershell
python manage.py collectstatic --noinput
```

  Set `USE_WHITENOISE=0` to opt out.
* `USE_MANIFEST_STATIC=1` switches to `CompressedManifestStaticFilesStorage`
  (`whitenoise.storage.CompressedManifestStaticFilesStorage`) so every
  collected asset gets a content hash in its name and `staticfiles.json`.
* `StaticCacheHeadersMiddleware` adds
  `Cache-Control: public, max-age=31536000, immutable` for hashed assets and
  `max-age=3600` for the rest. It wraps WhiteNoise, so the policy also applies
  to files WhiteNoise serves; with a pure CDN the request never reaches Django.

### Real user monitoring (RUM)

* The Vue client reports Core Web Vitals (LCP, CLS, INP) plus FCP and TTFB
  once per page load to `POST /api/admin/rum/` as
  `{ "metrics": [{ "name": "LCP", "value": 1234.5, "rating": "good", "page_path": "/production" }] }`.
  The beacon needs no authentication.
* Set `VITE_RUM=false` to disable collection.
* Admins can read the samples at `GET /api/admin/rum/` and the aggregated
  percentiles at `GET /api/admin/rum/summary/?days=7` (median/p75/p95, rating
  buckets and the top pages by sample count).
* The same summary is shown on the System Administration page as a
  "Web Vitals" card.

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

