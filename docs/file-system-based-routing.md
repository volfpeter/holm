# File-system based routing

`holm` uses a file-system based router, which means the structure of your project's directories and files automatically defines the routes of your application. This convention-over-configuration approach simplifies routing management and makes the project structure intuitive and predictable.

If you have experience with Next.js, you will find this routing paradigm very familiar.

Going through the [Application components](application-components.md) documentation is recommended before continuing this guide.

## Core concepts

- Packages define URL segments: Each Python package within your application's root maps to a URL segment. Nesting directories creates nested routes. For example, the `my_app/users/` package will create routes under the `/users` URL path.
- Special files mark application endpoints: `holm` looks for specific filenames within your application directory to discover pages, layouts, custom APIs, and compose your application.
  - `page.py`: Creates a publicly accessible URL for a route segment.
  - `layout.py`: Defines a shared UI that wraps a route segment and its children.
  - `api.py`: Creates custom API endpoints for a route segment.

## Routing conventions

Let's use the following project structure as an example to explore the routing conventions in `holm`.

```
my_app/
├── __init__.py
├── layout.py
├── main.py
├── navbar.py
├── page.py
├── users/
│   ├── __init__.py
│   ├── api.py
│   ├── layout.py
│   ├── page.py
│   └── _user_id_/
│       ├── __init__.py
│       └── page.py
└── _components/
    ├── __init__.py
    ├── page.py
    └── user/
        ├── __init__.py
        └── api.py
```

### Pages and layouts

A `page.py` file makes a route segment publicly accessible as (typically) a HTML page. Based on the example structure, `holm` will generate the following page routes:

- `my_app/page.py` creates the root route at `/`, because `page.py` is in the root application package.
- `my_app/users/page.py` creates the route at `/users`, because the page module is in the `users` package.
- `my_app/users/_user_id_/page.py` creates a dynamic route at `/users/{user_id}`, because this `page.py` is in the `users._user_id_` package and `_user_id_` marks a dynamic route segment.

Layouts defined in `layout.py` files automatically wrap layouts and pages within the same package and all subpackages.

- The layout in `my_app/layout.py` is the root layout, wrapping all layouts and pages.
- The layout in `my_app/users/layout.py` wraps the page at `/users` and the dynamic page at `/users/{user_id}`. The `users` layout is itself wrapped by the root layout.

### APIs

An `api.py` file allows you to define standard FastAPI API endpoints for a given route segment. These can be the usual JSON endpoints or [rendering APIs](guides/rendering-apis-with-htmx.md).

For example, `my_app/users/api.py` can define routes like `GET /count`, `POST /create`, which will be accessible under the `/users` path prefix (`/users/count`, `/users/create`).

`page.py` files automatically add a `GET /` route, and submit handlers a corresponding `POST /` route. To avoid path collision, it's recommended to avoid adding these routes in `api.py` files.

### Private packages

You can prevent a directory and all its subdirectories from being included in the routing system by prefixing its name with an underscore (`_`). This is useful for separating components, utilities, or other files that should not be routable.

In our example, the `_components/` directory is such a private package.

- `my_app/_components/page.py` will **not** create a route.
- `my_app/_components/user/api.py` will **not** create an API.

This allows you to organize your internal components logically without exposing them as endpoints.

*Note: A package name like `_user_id_` which is surrounded by underscores is treated as a [dynamic route segment](application-components.md#path-parameters-as-package-names), not a private package.*

### Colocation

Besides the special files (`page.py`, `layout.py`, `api.py`, etc.), you can place any other files within your application package (the package where `holm.App()` is called). `holm` will ignore them during route discovery. This allows you to colocate your business logic and UI components with your application components.

In the example, `my_app/navbar.py` is not a special file, so it is not routable. It can define any components or utilities, like a `Navbar`, which can then be imported and used in the layouts, pages, or APIs of the application.

`holm` also doesn't consider anything that's outside of the application package as an application component. We could create a `my_components/` directory next to `my_app/` and have anything in it, including `page.py` files for example. The content of this package would be ignored by `holm`, this package is not within the application package.

### Submit handlers

For any `page.py` file, you can also define a `handle_submit` function. This automatically creates a `POST` route at the same URL as the page. This is a convenient pattern for handling HTML form submissions that modify data.

If `my_app/users/page.py` defines a `handle_submit` function, it will handle `POST /users` requests, and the `page` function in the same file will handle `GET /users` requests as usual.
