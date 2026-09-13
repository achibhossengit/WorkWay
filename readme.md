![WorkWay introduction banner](./docs/intro-banner.png)

**WorkWay API** — job portal backend

[Live app](https://workway-client.vercel.app/) · [Live API](https://work-way.vercel.app/api/v1/) · [Swagger](https://work-way.vercel.app/api/v1/swagger/) · [ReDoc](https://work-way.vercel.app/api/v1/redoc/) · [Client Repo](https://github.com/achibhossengit/workway-client)

WorkWay is a full-stack job portal where employers post openings and manage applicants, and job seekers apply, track status, and review employers. Featured listings are sold through SSLCommerz.

This repository is the **backend API**. It handles users, jobs, applications, reviews, email notifications, media, and payments. Storage is PostgreSQL; production media uses Cloudinary.

Browse interactive docs on the live API: [Swagger](https://work-way.vercel.app/api/v1/swagger/) · [ReDoc](https://work-way.vercel.app/api/v1/redoc/).

## ✨ Key Features

- REST APIs for jobs, categories, employers, jobseekers, applications, reviews, and payments.
- JWT auth via Djoser + SimpleJWT (registration, activation, password reset).
- Role model: **Employer** and **Jobseeker** profiles created on signup.
- Applications: Pending / Reviewed / Accept / Rejected / Cancelled; soft cancel + re-apply.
- Emails on apply, re-apply, cancel (to employer) and status change (to jobseeker).
- Reviews: jobseekers rate employers after a finished application; public review list.
- Featured jobs: SSLCommerz payment extends `featured_until`.
- Paginated list endpoints (`page`, optional `page_size`).



## 🚀 Tech Stack


| Category   | Technology                                      |
| ---------- | ----------------------------------------------- |
| Runtime    | Python, Django 5.2, Django REST Framework       |
| Auth       | Djoser, SimpleJWT (`Authorization: JWT …`)      |
| Database   | PostgreSQL (`DATABASE_URL` via dj-database-url) |
| Media      | Local disk (DEBUG) / Cloudinary (production)    |
| Email      | Django SMTP (e.g. MailHog locally)              |
| Payments   | SSLCommerz                                      |
| Docs       | drf-yasg (Swagger / ReDoc)                      |
| Deployment | Vercel (`WorkWay.wsgi.app`), WhiteNoise         |




## 🛠️ Installation & Setup

```bash
git clone https://github.com/achibhossengit/workway-api.git
cd workway-api
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Optional Docker services (Postgres + MailHog):

```bash
docker compose up -d
```

Create a `.env` file in the project root:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

DATABASE_URL=postgres://workway:workway@localhost:5432/workway

CLOUD_NAME=
API_KEY=
API_SECRET=

EMAIL_FRONTEND_PROTOCOL=http
EMAIL_FRONTEND_DOMAIN=localhost:5173
EMAIL_FRONTEND_SITE_NAME=WorkWay

EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

SSL_STORE_ID=
SSL_STORE_PASSWD=
SSL_IS_SANDBOX=True
SSL_BACKEND_URL=http://127.0.0.1:8000
SSL_FRONTEND_URL=http://localhost:5173
```

```bash
python manage.py migrate
python manage.py loaddata employers jobseekers categories jobs applications reviews
python manage.py runserver
```

Local base: [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)


| Resource            | URL                                            |
| ------------------- | ---------------------------------------------- |
| Swagger             | `/api/v1/swagger/`                             |
| ReDoc               | `/api/v1/redoc/`                               |
| Admin               | `/admin/`                                      |
| MailHog UI (Docker) | [http://localhost:8025](http://localhost:8025) |




## 📁 Project Structure

```text
api/              Routers, permissions, API wiring
users/            CustomUser, Employer, JobSeeker
jobs/             Category, Job, details, requirements
apply_review/     Application, Review, email signals
payments/         SSLCommerz featured-job flow
WorkWay/          Settings, URLs, WSGI (`app` for Vercel)
fixtures/         Seed data
docker-compose.yml
vercel.json
docs/             README intro banner
manage.py
requirements.txt
```



## ⚙️ Workflows



### 1. Authentication

- Registration creates the matching Employer or Jobseeker profile.
- Activation and password-reset emails use `EMAIL_FRONTEND_*` links.
- Clients authenticate with JWT (`Authorization: JWT <access>`).



### 2. Jobs & applications

- Public job list supports category and search filters; featured jobs sort first.
- Employers manage their postings and applicant statuses.
- Jobseekers apply, cancel (soft), and re-apply when allowed.



### 3. Reviews & featured payments

- After Accept or Rejected, a jobseeker may leave one review per employer.
- Featured-job checkout runs through SSLCommerz and extends `featured_until`.



## 🗃️ Database

PostgreSQL via `DATABASE_URL` (example: `postgres://USER:PASSWORD@HOST:PORT/NAME`).


| App            | Main models                                |
| -------------- | ------------------------------------------ |
| `users`        | `CustomUser`, `Employer`, `JobSeeker`      |
| `jobs`         | `Category`, `Job`, `Detail`, `Requirement` |
| `apply_review` | `Application`, `Review`                    |
| `payments`     | `Payment`                                  |




## 🌐 Deployment

The API is deployed on **Vercel** using `vercel.json` and the WSGI entry `WorkWay.wsgi.app`.

1. Push this repo to GitHub and import the project in Vercel.
2. Set the same environment variables as `.env` (production values):
  - `SECRET_KEY`, `DEBUG=False`
  - `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
  - `DATABASE_URL` (hosted Postgres)
  - `CLOUD_NAME`, `API_KEY`, `API_SECRET` (Cloudinary media)
  - `EMAIL_*` and `EMAIL_FRONTEND_*` (real SMTP + live client domain)
  - `SSL_*` payment settings with public `SSL_BACKEND_URL` / `SSL_FRONTEND_URL`
3. Deploy. Vercel builds from `WorkWay/wsgi.py` (Python 3.11).
4. Run migrations against the production database (`python manage.py migrate`) from a machine that can reach `DATABASE_URL`.

Static files are served with **WhiteNoise**. With `DEBUG=False`, uploaded media uses **Cloudinary**.