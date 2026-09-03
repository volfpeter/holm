# Application design

This document explains how the application is put together: why the files, tasks, and configuration exist, and how the pieces work together during development and deployment. The design page at `/design` presents the same content in the running application.

## The stack

The application is a standard [FastAPI](https://fastapi.tiangolo.com) app, assembled with [holm](https://volfpeter.github.io/holm):

- Routing and layout composition are `holm`'s job: it walks the `app/` package and turns modules into routes, layouts, and actions. There are no routes to register manually.
- Rendering happens server-side with [htmy](https://volfpeter.github.io/htmy): typed, async Python components with JSX-like syntax, plus optional Jinja layouts.
- Dynamic updates use [HTMX](https://htmx.org): endpoints return HTML fragments that the browser swaps in. There is no client-side JavaScript framework.
- Styling uses [TailwindCSS](https://tailwindcss.com) utility classes.
- Accessible components come from [BasecoatUI](https://basecoatui.com), vendored into `components/` by [htmui](https://github.com/volfpeter/htmui).

Everything is server-rendered Python. The browser receives that HTML plus static assets: the stylesheet and the JS bundle. If you are new to `holm`, the [holm in a hurry](https://volfpeter.github.io/holm/in-a-hurry) guide covers the essentials in under five minutes.

## Directory layout

```text
.
├── app/                 # The application package — holm walks this for routes
│   ├── main.py          # FastAPI app + holm App wiring, static files, layout slots
│   ├── settings.py      # pydantic-settings; which CSS/JS files to serve
│   ├── head.py          # The <head> component, with page metadata support
│   ├── nav.py           # Root navigation bar, highlights the current page
│   ├── layout.py        # Root layout: renders layout.jinja (optional, see below)
│   ├── layout.jinja     # Root layout markup
│   ├── page.py          # Landing page
│   ├── actions.py       # HTMX endpoints returning HTML fragments
│   ├── page.html        # Static markup for the landing page
│   ├── design/          # The design page at /design, based on this document
│   │   ├── page.py
│   │   └── page.html
│   ├── showcase/        # The vendored component catalog in action, at /showcase
│   │   └── page.py
│   └── __init__.py
├── assets/              # Source files for the stylesheet and JS bundle
│   ├── app.css          # Tailwind input — your CSS goes here
│   └── app.js           # JS entry point — your scripts go here
├── components/          # htmui BasecoatUI catalog — plain Python, you own it
├── static/              # Build outputs, served at /static
├── .agents/skills/      # The holm-web agent skill
├── Procfile             # Process definitions for honcho (poe start)
├── package.json         # JS tooling only (Tailwind, HTMX, esbuild) — no app code
└── pyproject.toml       # Python dependencies, tool config, poe tasks
```

Two things to watch out for: `holm`'s route discovery walks `app/`, so every `page.py`, `layout.py`, and `actions.py` under it becomes a route. UI components therefore live in `components/` at the project root, outside `app/`, where discovery never touches them. Import them as `from components import button`.

Similarly, `assets/` and `static/` have different roles: `assets/` holds the sources you edit, `static/` the build outputs the app serves. Nothing in `static/` should be edited by hand.

## Agent support

The project ships the `holm-web` agent skill in `.agents/skills/`. Agents should load it before working on the application: it documents holm's routing, layout, page, action, and form conventions, and can answer questions about the library itself. The skill is maintained upstream and installed automatically. See the `holm skill` CLI command for managing it in other projects.

## The application package

`app/main.py` is the composition root: it creates the `FastAPI` app, mounts `static/` at `/static`, adds gzip compression, and hands everything to `holm.App()`. Custom FastAPI middleware, exception handlers, or additional mounts belong there.

Layout slots are configured in the same call. The root layout renders three named slots besides `children`: `head` (the `<head>` component from `app/head.py`), `nav` (the current-page-aware navigation bar from `app/nav.py`), and `theme_switcher`. Nested layouts can define further slots. `app/head.py` gets access to page metadata through the `htmy` context: it is a context-only component that reads the metadata the current page put there.

`app/settings.py` holds runtime settings via pydantic-settings, reading `.env` when present. It selects which stylesheet and JS bundle to serve through the `CSS_FILE` and `JS_FILE` environment variables, which is the mechanism behind `poe dev` and `poe preview`.

Within `app/`, `holm`'s conventions apply: `page.py` serves GET requests for its package's path, `layout.py` (or `layout.jinja`) wraps the pages of its package and everything below it, and `actions.py` defines endpoints for HTMX partials. `app/layout.py` is optional. `holm` renders `layout.jinja` on its own when no Python counterpart exists; the file exists to make the mechanism explicit and to serve as a starting point for programmatic layouts. The conventions are documented in the `holm` docs and the agent skill.

## Stylesheets and scripts

There is no bundler for application code. Python components are served as-is, and only two artifacts are built: the Tailwind stylesheet and the JS bundle.

Sources live in `assets/`:

- `app.css` imports TailwindCSS and BasecoatUI and defines the component classes used by the scaffold's own pages — remove them along with those pages. Your own CSS goes here.
- `app.js` imports HTMX and the BasecoatUI runtime. Your own scripts go here.

Both are compiled into `static/` in two flavors:

- `app-dev.css` / `app-dev.js` are unminified, rebuilt on every save by the watchers, and served in development.
- `app.css` / `app.js` are minified, built ahead of deployment, and served in production.

The minified files are part of the working tree on purpose: a fresh checkout contains everything needed to run and deploy the application. The dev files are build artifacts that can be deleted and regenerated at any time.

Which pair is served is decided by `CSS_FILE` and `JS_FILE` from `app/settings.py`, rendered into `<head>` by `app/head.py`.

All build commands are defined as poe tasks in `pyproject.toml` (`build-dev-css`, `build-prod-css`, `build-dev-js`, `build-prod-js`) and delegate to the Tailwind CLI and the JS bundler. `poe build` runs the production builds in one go. The `package.json` exists only for these tools. There is no application JavaScript beyond what `assets/app.js` imports.

The `components/` directory holds the full [htmui](https://github.com/volfpeter/htmui) BasecoatUI catalog, vendored: a copy in the project, not a dependency. Everything is already set up and ready to use — explore it, and edit the copies freely when you want to customize them.

## Development workflow

`uv run poe start` runs three processes together via [honcho](https://github.com/nickstenning/honcho), as defined in `Procfile`:

1. The application (`fastapi dev`, with auto-reload)
2. The Tailwind watcher rebuilding `static/app-dev.css`
3. The JS watcher rebuilding `static/app-dev.js`

The app is the first process in the `Procfile`, and honcho assigns ports to processes in that order, so the app gets port 5000. Run the application standalone (for example `uv run poe dev` or `fastapi dev`) and it comes up on the FastAPI default port instead, which is 8000.

The two standalone app tasks differ in what they serve:

- `poe dev` serves the dev stylesheet and JS bundle, which the watchers keep current.
- `poe preview` serves the minified files, which is what will be deployed. Use it to verify production assets.

Edit `assets/`, `app/`, or `components/`, save, refresh. Auto-reload and the watchers handle the rest.

## Tooling and quality

Python dependencies are managed by [uv](https://docs.astral.sh/uv/), locked in `uv.lock`. Formatting and linting use [ruff](https://docs.astral.sh/ruff/), type checking [mypy](https://mypy-lang.org/) in strict mode. All recurring commands are poe tasks; `poe check` runs all checks in one go.

## Deployment

Deployments serve `static/app.css` and `static/app.js`, so build them first:

```bash
uv run poe build
```

Two providers work out of the box, no configuration needed. The `[tool.fastapi]` entrypoint in `pyproject.toml` points them at `app.main:app`:

- Vercel: import the repository.
- FastAPI Cloud: `uv run fastapi deploy`.

Beyond that, a `holm` application is a plain FastAPI application — deploy it however you like.
