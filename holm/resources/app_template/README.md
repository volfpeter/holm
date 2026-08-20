# **holm_name**

A [holm](https://volfpeter.github.io/holm) application: file-system based routing, server-side rendering with [htmy](https://volfpeter.github.io/htmy), dynamic page updates with [HTMX](https://htmx.org), and [BasecoatUI](https://basecoatui.com) components vendored with [htmui](https://github.com/volfpeter/htmui).

## Run

    uv run poe start          # http://localhost:5000

`poe start` runs three processes (see `Procfile`): the app (`fastapi dev`, auto-reload), the Tailwind watcher that rebuilds `static/app-dev.css`, and the JS watcher that rebuilds `static/app-dev.js`.

To run only the app: `uv run poe dev` serves it with the dev stylesheet and JS bundle, `uv run poe preview` with the minified ones — what will actually be deployed.

## Backend (Python)

Python dependencies are managed by [uv](https://docs.astral.sh/uv/) in `pyproject.toml` (locked in `uv.lock`, installed into `.venv/`).

The application is the `app/` package. holm walks it and turns modules into routes:

- `page.py` — a page. `app/page.py` serves `GET /`; `app/user/page.py` would serve `GET /user`. Every `page.py` anywhere under `app/` becomes a URL.
- `layout.py` and `layout.jinja` — the layout that wraps the pages of its package and everything nested below it. The markup is in the Jinja template; `layout.py` renders it with `holm.JinjaTemplate` and is optional — delete it and holm picks up and renders `layout.jinja` on its own. The `head` and `theme_switcher` slots it uses are default slots, configured in `app/main.py`.
- `actions.py` — actions, endpoints that return HTML fragments for HTMX.

Start with `app/page.py` (the landing page) and `app/actions.py` (the action behind the tip that rotates every 4 seconds). Rendering uses htmy: components are plain Python functions and expressions, no template language to learn.

UI components are **not** inside `app/`. They live in `components/` at the project root, next to `app/`, so holm's route discovery never touches them. Import them as `from components import dialog`.

Tooling is [ruff](https://docs.astral.sh/ruff/) for formatting and linting, [mypy](https://mypy-lang.org/) in strict mode for type checking, and [poethepoet](https://github.com/nat-n/poethepoet) for tasks:

- `poe start` — app, CSS watcher, and JS watcher, via [honcho](https://github.com/nickstenning/honcho)
- `poe dev` / `poe preview` — app only, with the dev / minified stylesheet and JS bundle
- `poe build-dev-css` / `poe build-prod-css` — one-off stylesheet builds
- `poe build-dev-js` / `poe build-prod-js` — one-off JS bundle builds
- `poe format` / `poe lint` / `poe types` — checks; `format-fix` and `lint-fix` apply fixes
- `poe check` — all checks in one go

Which stylesheet and JS bundle are served is controlled by the `CSS_FILE` and `JS_FILE` environment variables (see `app/settings.py`).

## Frontend (CSS and JS)

Styles are [TailwindCSS](https://tailwindcss.com) v4 with [BasecoatUI](https://basecoatui.com) on top. JavaScript is [HTMX](https://htmx.org) plus Basecoat's runtime — no JavaScript framework. Both are built from source:

- `assets/app.css` — the Tailwind input: the Tailwind and BasecoatUI imports plus a few example component classes. This is where your own CSS goes.
- `assets/app.js` — the JS entry: HTMX and Basecoat imports. This is where your own scripts go.
- `static/app-dev.css` / `static/app-dev.js` — unminified builds, served by `poe dev`.
- `static/app.css` / `static/app.js` — minified builds, served by `poe preview` and in deployment.

The minified builds are part of the working tree. The unminified ones are produced by the watchers when you `poe start`.

`components/` holds the BasecoatUI component catalog, vendored by `htmui`. Components are plain Python — import and call them, e.g. `button.button("Save")`. Pull in more with:

    uvx htmui init -c dialog

The built stylesheet and script are wired up in `app/head.py`.

## Deploy

Deployments serve `static/app.css` and `static/app.js`, so build them first:

    uv run poe build-prod-css
    uv run poe build-prod-js

- **Vercel**: import the repository — no configuration needed, `[tool.fastapi]` in `pyproject.toml` is the entrypoint.
- **FastAPI Cloud**: `uv run fastapi deploy`.
