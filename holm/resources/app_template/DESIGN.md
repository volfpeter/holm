# Application design

This document explains how the application is put together: why the files, tasks, and configuration exist, and how the pieces work together during development and deployment.

## The stack

The application is a standard [FastAPI](https://fastapi.tiangolo.com) app, assembled with [`holm`](https://volfpeter.github.io/holm):

- Routing and layout composition are `holm`'s job: it walks the `app/` package and turns modules into routes, layouts, and actions. There are no routes to register manually.
- Rendering happens server-side with [`htmy`](https://volfpeter.github.io/htmy): typed, async Python components with JSX-like syntax, plus optional Jinja layouts.
- Dynamic updates use [HTMX](https://htmx.org): endpoints return HTML fragments that the browser swaps in. There is no client-side JavaScript framework.
- Styling uses [TailwindCSS](https://tailwindcss.com) utility classes.
- Accessible components come from [BasecoatUI](https://basecoatui.com). [`htmui`](https://github.com/volfpeter/htmui) copies a pure Python `htmy` implementation into `components/`; those files are yours to edit.

Pages render on the server. The browser receives that HTML plus the stylesheet and the JS bundle. If you are new to `holm`, the [holm in a hurry](https://volfpeter.github.io/holm/in-a-hurry) guide covers the essentials in under five minutes.

## Directory layout

```text
.
├── .agents/skills/      # holm-web agent skill
├── app/                 # Application package; holm walks this
│   ├── main.py          # FastAPI app, holm wiring, static files, layout slots
│   ├── settings.py      # pydantic-settings; which CSS/JS files to serve
│   ├── head.py          # <head> component, with page metadata support
│   ├── error.py         # Error handlers; 404 redirects to /not-found
│   ├── layout.py        # Root layout; renders layout.jinja (optional)
│   ├── layout.jinja     # Root layout markup
│   ├── not_found/       # Not-found page package (served at /not-found)
│   │   └── page.py
│   └── page.py          # Home page
├── assets/              # Stylesheet and JS bundle sources
│   ├── app.css          # Tailwind input; your CSS goes here
│   └── app.js           # JS entry point; your scripts go here
├── components/          # BasecoatUI as Python; yours to edit
├── static/              # Build outputs, served at /static
├── Procfile             # honcho process definitions (poe start)
├── package.json         # Tailwind, HTMX, and the JS bundler
└── pyproject.toml       # Python dependencies, tool config, poe tasks
```

`holm` walks `app/`: `page.py` becomes a route, `layout.py` or `layout.jinja` wraps pages, `actions.py` defines endpoints that return HTML fragments, and `error.py` maps error codes to handlers (the 404 handler redirects to `/not-found`). UI components live in `components/` at the project root, outside `app/`, where discovery never touches them. Import them as `from components.button import button`. The full template additionally ships `app/nav.py`, `app/actions.py`, `app/design/`, `app/showcase/`, and `assets/demo.css`; delete what you don't need.

`assets/` holds the source files for the stylesheet and the JS bundle; you edit those. `static/` holds the compiled files the app serves. Don't edit anything in `static/` by hand.

## Agent support

The project ships the `holm-web` agent skill in `.agents/skills/`. Agents should load it before working on the application: it documents holm's routing, layout, page, action, and form conventions, and can answer questions about the library itself. See the `holm skill` CLI command for managing it in other projects.

## The application package

`app/main.py` is the composition root: it creates the FastAPI app, mounts `static/` at `/static`, adds gzip compression, and hands everything to `holm.App()`. Custom FastAPI middleware, exception handlers, or additional mounts belong there.

Layout slots are configured in the same call. The root layout renders two named slots besides `children`: `head` (the `<head>` component from `app/head.py`) and `theme_switcher`. The full template adds a third slot, `nav` (the current-page-aware navigation bar from `app/nav.py`). Nested layouts can define further slots. `app/head.py` gets access to page metadata through the `htmy` context: it is a context-only component that reads the metadata the current page put there.

`app/settings.py` holds runtime settings via pydantic-settings, reading `.env` when present. It selects which stylesheet and JS bundle to serve through the `CSS_FILE` and `JS_FILE` environment variables, which is the mechanism behind `poe dev` and `poe preview`.

Within `app/`, `holm`'s conventions apply: `page.py` serves GET requests for its package's path, `layout.py` (or `layout.jinja`) wraps the pages of its package and everything below it, and `actions.py` defines endpoints that return HTML fragments, a natural fit for HTMX. `app/layout.py` is optional. `holm` renders `layout.jinja` on its own when no Python counterpart exists; the file exists to make the mechanism explicit and to serve as a starting point for programmatic layouts. The conventions are documented in the `holm` docs and the agent skill.

## Stylesheets and scripts

Only the stylesheet and the JS bundle are built from `assets/`.

Sources live in `assets/`:

- `app.css` imports TailwindCSS and BasecoatUI. Your own CSS goes here. The full template keeps its demo styles in `assets/demo.css`, imported from `app.css`; delete that file together with the demo pages.
- `app.js` imports HTMX and the BasecoatUI runtime. Your own scripts go here.

Both are compiled into `static/` in two flavors:

- `app-dev.css` / `app-dev.js` are unminified, rebuilt on every save by the watchers, and served in development.
- `app.css` / `app.js` are minified, built ahead of deployment, and served in production.

The minified files belong in the repo so a fresh checkout can run and deploy without a production build. The dev files are build artifacts that can be deleted and regenerated at any time.

Which pair is served is decided by `CSS_FILE` and `JS_FILE` from `app/settings.py`, rendered into `<head>` by `app/head.py`.

All build commands are defined as `poe` tasks in `pyproject.toml` (`build-dev-css`, `build-prod-css`, `build-dev-js`, `build-prod-js`) and delegate to the Tailwind CLI and the JS bundler. `poe build` runs the production builds in one go. The `package.json` exists for these tools. There is no application JavaScript beyond what `assets/app.js` imports.

The `components/` directory is a copy of the [`htmui`](https://github.com/volfpeter/htmui) BasecoatUI catalog: pure Python `htmy` components in your project, not a locked dependency. Open a file and change it. Import them as `from components.button import button`.

## Development workflow

`uv run poe start` runs three processes together via [`honcho`](https://github.com/nickstenning/honcho), as defined in `Procfile`:

1. The application (`fastapi dev`, with auto-reload)
2. The Tailwind watcher rebuilding `static/app-dev.css`
3. The JS watcher rebuilding `static/app-dev.js`

The app is the first process in the `Procfile`, and `honcho` assigns ports to processes in that order, so the app gets port 5000. Edit `assets/`, `app/`, or `components/`, save, refresh.

Run the application standalone (for example `uv run poe dev` or `fastapi dev`) and it comes up on the FastAPI default port instead, which is 8000.

- `poe dev` serves the dev stylesheet and JS bundle.
- `poe preview` serves the minified files, which is what will be deployed. Use it to verify production assets.

## Tooling and quality

Python dependencies are managed by [`uv`](https://docs.astral.sh/uv/), locked in `uv.lock`. Formatting and linting use [`ruff`](https://docs.astral.sh/ruff/), type checking [`mypy`](https://mypy-lang.org/) in strict mode. All recurring commands are `poe` tasks; `poe check` runs all checks in one go.

## Deployment

A `holm` application is a plain FastAPI application, so it deploys anywhere FastAPI is supported as a first-class citizen. Deployments serve `static/app.css` and `static/app.js`, so build them first:

```bash
uv run poe build
```

Providers that support the `[tool.fastapi]` configuration in `pyproject.toml` work out of the box with no extra configuration, for example:

- Vercel: import the repository.
- FastAPI Cloud: `uv run fastapi deploy`.
