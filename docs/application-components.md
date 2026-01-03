# Application components

This section summarizes the different components of `holm` applications. If you have used Next.js before, you will find these concepts very familiar. If not, don't worry, they may seem complex at first, but they are quite intuitive and natural.

## Layouts and pages

*Layouts* are defined in the `layout.py` modules of packages as a callable `layout` variable (note that for example classes with an `__init__()` method, or `htmy.Component`s are callable, so they also qualify).

Rules for *layouts*:

- The root layout must always return a `htmy.Component`.
- `layout` must be a callable and it must accept a positional argument (other than `self` if the layout is a method of a class), the data / properties of the layout that are returned by the pages or layouts this layout directly wraps.
- `layout` can have additional arguments (position or keyword and keyword-only, but not positional-only). These arguments must be FastAPI dependencies. They will be automatically resolved during each request.
- Returning a tuple or a list from a layout is **not allowed** unless the value is a `htmy.ComponentSequence`. Tuples and lists are always interpreted and treated as component sequences, so you don't need to track what kinds of components pages and layouts return. See `htmy.is_component_sequence()` for more information.

By default, layouts automatically wrap all layouts and pages in subpackages. You can opt out of this behavior by wrapping the return value of a layout or page with the [`without_layout` utility](utilities.md#without_layout).

*Tip: layouts can provide context for their entire subtree by wrapping the subtree with a `htmy` `ContextProvider` component.*

*Pages* are defined in the `page.py` module of packages as a callable `page` variable (note that classes with an `__init__()` method are callable, so they also qualify).

Rules for *pages*:

- `page` must be a FastAPI dependency, meaning it can have any arguments as long as they can all be resolved by FastAPI as dependencies.
- `page` must return the properties object for the layout that directly wraps it.
- If a page is not wrapped by a layout, then it must return a `htmy.Component`.
- Returning a tuple or a list from a page is **not allowed** unless the value is a `htmy.ComponentSequence`. Tuples and lists are always interpreted and treated as component sequences, so you don't need to track what kinds of components pages and layouts return. See `htmy.is_component_sequence()` for more information.
- `page` can directly return a FastAPI `Response` as well, which is always returned as is.

### Page metadata

`page.py` modules can have a `metadata` variable, which can be an arbitrary mapping or a FastAPI dependency that returns an arbitrary mapping.

If the `metadata` variable is a callable, it can have any FastAPI dependencies, even different ones than what the `page` or wrapper layouts use.

The metadata provided by the currently served page is made available to every `htmy.Component` (from the root layout to the page itself) through the built-in `Metadata` utility. It can be accessed as `Metadata.from_context(context)` where `context` is the `htmy` rendering context which is passed to every component. See the [htmy documentation](https://volfpeter.github.io/htmy/#context) for more information.

This feature is particularly useful when page-specific information - for example title, description, or keywords - must be set dynamically (for example, in layouts) on a page-by-page basis. `Metadata` implements the `Mapping` protocol, so once loaded from the `htmy` rendering context in a component with `metadata = Metadata.from_context(context)`, you can use it simply like this to set page-specific information in any layout, component, or the page itself: `htmy.html.title(metadata["title"])`.

### Page submit handlers

`page.py` modules can also define a callable `handle_submit` variable. The same rendering logic and rules apply to it as to the `page` variable itself. The only difference is that for `handle_submit`, a HTTP `POST` route is created.

`handle_submit`, together with `page`, offer a convenient way to handle form submission in your application.

The default HTML `<form>` action is to submit the form to the current URL using a HTTP GET request. This means if you have a form in your `page` (or `layout`), and you do not set `action` and `method`, your form's submission will be handled by your current `page` by default (your GET route). This is useful for search and filtering forms for example.

For forms that trigger state change on the server, you should set the form `method` to `POST`. This is important from a CSRF prevention perspective, and it also ensures the submitted form will be handled by your `handle_submit` function (your POST route), instead of your `page` function.

You can of course set `action` to some URL. In that case the same logic applies, but instead of triggering the `page` or `handle_submit` function that belong to the current URL, it will trigger them in the `page.py` or `api.py` module that handles the given URL.

## Actions

*Actions* provide a convenient and flexible way to create custom HTML rendering routes that don't fit the standard `page` pattern. They are functions decorated with one of the `@action` decorators (`@action.get()`, `@action.post()`, etc.), and they can be defined in either a `page.py` or `actions.py` module.

Rules for *actions*:

- An action must be a FastAPI dependency, just like a page.
- Actions can be registered with any HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), using the appropriate `@action` decorator.
- You can specify a custom URL path for an action (e.g., `@action.post("/do-something")`), but it is optional. If no path is provided, the function's name is used as the path, with underscores (`_`) being replaced by hyphens (`-`). In both cases, the path is relative to the URL corresponding to the package that contains the action.
- By default, components returned from actions are not wrapped in layouts. This is ideal for returning HTML fragments for client frameworks like HTMX.
- To render an action's return value in its owner layouts (like it is done by default for pages), you can set `use_layout=True` in the decorator: `@action.get(use_layout=True)`. This behavior can of course be combined with the [`without_layout` utility](utilities.md#without_layout).
- Actions can also have `metadata`: `@action.get(metadata={"title": "Hello"})`. `metadata` works identically to page metadata and is particularly useful when combined with `use_layout`.
- An action can directly return a FastAPI `Response`, which is always returned as is.

## APIs

APIs are defined in the `api.py` module or packages as an `APIRouter` variable or a callable that returns an `APIRouter`.

`api.py` modules serve two primary use-cases:

- They allow creating a custom `APIRouter` configuration for the package, for example by adding `APIRouter` dependencies.
- They allow creating standard FastAPI routes that serve JSON.

These are standard FastAPI `APIRouter`s, but you should still follow these recommendations:

- If routes in the API don't do any rendering, then the `api()` callable should have no arguments or simply an `api` variable should be used.
- If the API has rendering routes, the `api()` callable should have a single `fasthx.htmy.HTMY` positional argument. The application's renderer will be passed to this function automatically by `holm`.
- If an `api()` callable is used, it may have further arguments as long as they all have default values. This pattern can simplify API testing for example, by allowing custom configurations for tests.

Note on rendering APIs:

- They are a lower-level alternative to [actions](#actions). In most cases, you should prefer using actions instead: they are simpler and more powerful.
- The primary role of these APIs is to return so called "partials" (small HTML snippets instead of entire HTML pages) to clients such as HTMX for swapping.
- The components returned by rendering routes are not automatically wrapped in layouts like pages are.

## Path parameters as package names

Routes with path parameters, also often referred to as "dynamic routes", are essential to almost all applications. A simple example is a user profile page, served at `/user/{id}` for example, where we want to display information about the user with the given ID.

You can capture dynamic URL path parameters by using special package names. Two formats are supported:

- `_param_` format: package names like `_id_` or `_user_id_`.
- `{param}` format: package names like `{id}` or `{user_id}`. *(Note: it works with `holm`, but static code analysis tools flag it because `{id}` is not a valid Python identifier.)*

Both formats are converted to FastAPI path parameters. For example:

- File path `user/_id_/page.py` becomes URL `/user/{id}`.
- File path `user/{user_id}/settings/page.py` becomes URL `/user/{user_id}/settings`.

Any layout or page within these packages can access the path parameter as a FastAPI dependency by adding it to their function signature (e.g., `id: int` or `user_id: str`).

## Private packages

You can prefix package names with one or more underscores to opt the entire package (including its subpackages) out of the automatic application component discovery.

For example, if you have a package named `_private` somewhere in your application folder, you can freely place valid page, layout, or API files within it or its subpackages. These modules will not be processed and included in the application.

Reminder: if the package name also ends with an underscore, it will be treated as a path parameter, as described [above](#path-parameters-as-package-names).

## Error handling

Error handlers are defined in the `error.py` or `errors.py` module of the root package as a `handlers` variable, which can be a mapping from exception types or HTTP status codes to standard FastAPI exception handler functions, or a callable that expects a `fasthx.htmy.HTMY` positional argument and returns such a mapping. The latter option is useful if you want to do custom HTML rendering in an error handler.

Error handlers must return either a `htmy.Component` or a `fastapi.Response`. Responses are returned to the client as is, and components are automatically rendered and returned as a `HTMLResponse`.

It is important to know that rendered errors are **not** automatically wrapped in the root layout of your application. The main reason for this is `holm` can not always know what the client (be it HTMX or simply the browser) expects.

The recommended way to handle this is to create an HTML skeleton component somewhere in your codebase, and use it both in the root layout and in error handlers to wrap page content. This, together with application-specific exceptions make it easy to handle every error correctly with minimal manual effort.

Also, you can simply return redirect responses in error handlers that navigate users to the appropriate error page, passing context as query parameters.
