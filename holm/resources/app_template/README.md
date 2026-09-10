# __holm_name__

A [holm](https://volfpeter.github.io/holm) application: file-system based routing, server-side rendering with [`htmy`](https://volfpeter.github.io/htmy), dynamic page updates with [HTMX](https://htmx.org), and [BasecoatUI](https://basecoatui.com) components from [`htmui`](https://github.com/volfpeter/htmui).

[DESIGN.md](DESIGN.md) explains how the application is put together.

## Run

```bash
uv run poe start          # http://localhost:5000
```

`poe start` runs three processes (see `Procfile`):

- the app (`fastapi dev`, auto-reload)
- the Tailwind watcher that rebuilds `static/app-dev.css`
- the JS watcher that rebuilds `static/app-dev.js`.

Edit `assets/`, `app/`, or `components/`, save your changes, and reload the page to see the fresh version.

Use `uv run poe dev` to run only the app. It serves the app with the dev stylesheet and JS bundle. `uv run poe preview` uses the minified stylesheet and JS bundle, matching the config that would be deployed. These commands start the app on the FastAPI default port (8000).

## Where things live

- `app/`: the application package, the one `holm` walks. A `page.py` becomes a route, a `layout.py` or `layout.jinja` wraps pages, and `actions.py` defines endpoints that return HTML fragments (a natural fit for HTMX).
- `components/`: BasecoatUI as pure Python `htmy` components, copied into the project by [`htmui`](https://github.com/volfpeter/htmui). They live in your repo, so you can open and change them. These are outside `app/`, so the `holm` discovery process never treats them as routes. Example: `from components.button import button` then `button("Save")`.
- `assets/`: source files for the stylesheet and the JS bundle. Edit `app.css` for Tailwind and your own CSS, and `app.js` for HTMX, Basecoat, and your own scripts. Watchers and build tasks compile these into `static/`.
- `static/`: the compiled stylesheet and JS bundle, served at `/static` by FastAPI. Do not edit these files; change `assets/` and rebuild. The minified `app.css` and `app.js` belong in the repo so a checkout can run and deploy without a production build.

Rendering uses [`htmy`](https://volfpeter.github.io/htmy): JSX-like Python components.

## Tasks

Tooling is [`ruff`](https://docs.astral.sh/ruff/) for formatting and linting, [`mypy`](https://mypy-lang.org/) in strict mode for type checking, and [`poethepoet`](https://github.com/nat-n/poethepoet) for tasks:

- `poe start`: app, CSS watcher, and JS watcher, via [`honcho`](https://github.com/nickstenning/honcho)
- `poe dev` / `poe preview`: app only, with the dev / minified stylesheet and JS bundle
- `poe build`: both production builds in one go
- `poe build-dev-css` / `poe build-prod-css`: one-off stylesheet builds
- `poe build-dev-js` / `poe build-prod-js`: one-off JS bundle builds
- `poe format` / `poe lint` / `poe type`: checks; `format-fix` and `lint-fix` apply fixes
- `poe check`: all checks in one go

The served stylesheet and JS bundle are controlled by the `CSS_FILE` and `JS_FILE` environment variables (see `app/settings.py`).

The project ships the `holm-web` agent skill in `.agents/skills/`. Agents should load it automatically when working on the application.

## Deploy

A `holm` application is a plain FastAPI application, so it deploys anywhere FastAPI is supported as a first-class citizen. Deployments serve `static/app.css` and `static/app.js`, so build them first:

```bash
uv run poe build
```

Providers that support the `[tool.fastapi]` configuration in `pyproject.toml` work out of the box with no extra configuration, for example:

- **Vercel**: import the repository.
- **FastAPI Cloud**: `uv run fastapi deploy`.
