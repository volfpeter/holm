# **holm_name**

A [holm](https://volfpeter.github.io/holm) application: file-system based routing, server-side rendering with [htmy](https://volfpeter.github.io/htmy), dynamic page updates with [HTMX](https://htmx.org), and [BasecoatUI](https://basecoatui.com) components vendored with [htmui](https://github.com/volfpeter/htmui).

[DESIGN.md](DESIGN.md) explains how the application is put together — architecture, tooling, deployment internals. This file covers day-to-day use.

## Run

    uv run poe start          # http://localhost:5000

`poe start` runs three processes (see `Procfile`): the app (`fastapi dev`, auto-reload), the Tailwind watcher that rebuilds `static/app-dev.css`, and the JS watcher that rebuilds `static/app-dev.js`.

To run only the app: `uv run poe dev` serves it with the dev stylesheet and JS bundle, `uv run poe preview` with the minified ones — what will actually be deployed. Run the app on its own and it comes up on FastAPI's default port, 8000.

Edit `assets/`, `app/`, or `components/`, save, refresh — auto-reload and the watchers handle the rest.

## Where things live

- `app/` — the application. holm walks this package: every `page.py` becomes a route (`app/page.py` serves `GET /`, `app/design/page.py` serves `GET /design`), every `layout.py` or `layout.jinja` wraps its package's pages, every `actions.py` defines HTMX endpoints returning HTML fragments. Start with `app/page.py` (the landing page), `app/actions.py` (the action behind its rotating greeting), `app/design/` (the design page at `/design`, based on `DESIGN.md`), and `app/showcase/page.py` (the component showcase).
- `components/` — the full BasecoatUI catalog vendored by `htmui`, nothing to install. Plain Python: import and call them, e.g. `button.button("Save")`. Lives outside `app/` because holm's discovery walks `app/` only; edit the copies freely.
- `assets/` — the sources you edit: `app.css` (Tailwind input, your CSS goes here) and `app.js` (HTMX and Basecoat imports, your scripts go here).
- `static/` — build outputs served at `/static`. Never edit by hand. The minified builds are part of the working tree so a fresh checkout can run and deploy as-is.

Rendering uses [htmy](https://volfpeter.github.io/htmy): components are plain Python functions and expressions, no template language to learn. Jinja layouts are supported out of the box — see `app/layout.py` for a worked example.

## Tasks

Tooling is [ruff](https://docs.astral.sh/ruff/) for formatting and linting, [mypy](https://mypy-lang.org/) in strict mode for type checking, and [poethepoet](https://github.com/nat-n/poethepoet) for tasks:

- `poe start` — app, CSS watcher, and JS watcher, via [honcho](https://github.com/nickstenning/honcho)
- `poe dev` / `poe preview` — app only, with the dev / minified stylesheet and JS bundle
- `poe build` — both production builds in one go
- `poe build-dev-css` / `poe build-prod-css` — one-off stylesheet builds
- `poe build-dev-js` / `poe build-prod-js` — one-off JS bundle builds
- `poe format` / `poe lint` / `poe types` — checks; `format-fix` and `lint-fix` apply fixes
- `poe check` — all checks in one go

Which stylesheet and JS bundle are served is controlled by the `CSS_FILE` and `JS_FILE` environment variables (see `app/settings.py`).

The project ships the `holm-web` agent skill in `.agents/skills/` — agents should load it before working on the application.

## Deploy

Deployments serve `static/app.css` and `static/app.js`, so build them first:

    uv run poe build

- **Vercel**: import the repository — no configuration needed, `[tool.fastapi]` in `pyproject.toml` is the entrypoint.
- **FastAPI Cloud**: `uv run fastapi deploy`.

Beyond these, a `holm` application is a plain FastAPI application — deploy it however you like.
