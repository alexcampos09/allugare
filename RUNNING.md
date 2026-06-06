# Running allugare locally

`allugare` is a 2017 Django **1.11 / Python 3.6** rental-listings app (Brazilian
real-estate, pt-br). It originally deployed on Heroku with PostgreSQL and
served static/media from S3. This guide runs it locally with **zero external
services** — for portfolio screenshots or as a starting point for a client.

## TL;DR

```bash
docker compose up --build      # first build is slow (amd64 emulated on Apple Silicon)
open http://localhost:8010      # host port 8010 -> container 8000
```

That's it. The container migrates the DB, seeds demo data, and starts the dev
server. Admin login: **admin / admin** at http://localhost:8010/admin/.

## What the dev setup changes vs. production

Everything lives behind a dedicated, self-contained settings module,
`source/settings_dev.py` (`DJANGO_SETTINGS_MODULE=settings_dev`). The original
`allugare/settings/` package is left untouched — note it cannot be imported
as-is (its `__init__.py` eagerly imports `base`/`production`, which reference
files missing from this repo: `allugare.aws.conf` and `allugare.utils` storage
classes). `settings_dev` sidesteps that chain entirely and:

| Concern  | Production            | Local dev (`settings_dev`)         |
|----------|-----------------------|------------------------------------|
| Database | PostgreSQL (Heroku)   | SQLite (`source/db.sqlite3`)       |
| Storage  | AWS S3                | local disk (`source/static-live/`) |
| Email    | Gmail SMTP            | console backend                    |
| DEBUG    | off                   | on                                 |

CSS/JS come from public CDNs (Bootstrap 3, jQuery, Font Awesome) and still
load. Property *photos* were on S3 and are gone, so listings show Font Awesome
house/building placeholders.

## Demo data

`python manage.py seed_demo` (run automatically on container start, idempotent):
- superuser `admin` / `admin`
- a demo owner `corretora`
- 5 sample listings across SP / RJ / MG / PR
- a dummy Facebook `SocialApp` so the login/signup pages render (the templates
  reference the provider directly). It is **not** wired for real auth.

## Pages worth looking at

| URL                         | Page                                  |
|-----------------------------|---------------------------------------|
| `/`                         | marketing home (cityscape hero)       |
| `/sobre`                    | about                                 |
| `/lares/`                   | property listings (seeded)            |
| `/lares/1/`                 | listing detail (incl. Google Map)     |
| `/land/contact/`            | student landing + lead form           |
| `/accounts/login/`          | login (crispy-forms + FB button)      |
| `/admin/`                   | Django admin (admin / admin)          |

## Pointing at PostgreSQL (for a real client)

`settings_dev.py` has a commented `dj_database_url` block. Install
`dj-database-url` + `psycopg2`, set `DATABASE_URL`, and uncomment it. The full
original production pins are in `source/requirements.txt`.

## Secrets / configuration

All secrets are read from environment variables — nothing is hardcoded in the
tracked source. See `.env.example` for the full list (`DJANGO_SECRET_KEY`,
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, email + Google Maps keys). The
local demo (`settings_dev`) needs none of them: it uses a throwaway dev key,
the console email backend, and local-disk storage.

> ⚠️ **History note:** this repo's *git history* still contains the original
> 2017 secrets (a Django SECRET_KEY, AWS access keys, a Google Maps key, a
> Facebook app secret) from before they were removed from the working tree.
> Those keys must be treated as compromised and rotated/deactivated in their
> respective consoles. Scrubbing them from history requires a `git filter-repo`
> rewrite + force-push.

## Notes / cleanup TODO if productionizing

- The `allugare.aws.conf` / `allugare.utils` storage modules referenced by the
  original settings are missing and would need restoring for an S3 deploy.
