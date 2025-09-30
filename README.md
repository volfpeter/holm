![Tests](https://github.com/volfpeter/holm/actions/workflows/tests.yml/badge.svg)
![Linters](https://github.com/volfpeter/holm/actions/workflows/linters.yml/badge.svg)
![Documentation](https://github.com/volfpeter/holm/actions/workflows/build-docs.yml/badge.svg)
![PyPI package](https://img.shields.io/pypi/v/holm?color=%2334D058&label=PyPI%20Package)

**Source code**: [https://github.com/volfpeter/holm](https://github.com/volfpeter/holm)

**Documentation and examples**: [https://volfpeter.github.io/holm](https://volfpeter.github.io/holm/)

# holm

Web development framework that brings the Next.js developer experience to Python, built on FastAPI, `htmy`, and FastHX.

## Key features

- **Next.js**-like **developer experience** with **file-system based routing** and page composition.
- **Standard FastAPI** everywhere, so you can leverage the entire FastAPI ecosystem.
- **JSX-like syntax** with async support for components, thanks to `htmy`.
- First class **HTMX support** with `FastHX`.
- **Async** support everywhere, from APIs and dependencies all the way to UI components.
- Support for both **JSON** and **HTML** (server side rendering) APIs.
- **No JavaScript** dependencies
- **No build steps**, just server side rendering with **fully typed Python**.
- **Stability** by building only on the core feature set of dependent libraries.
- **Unopinionated**: use any CSS framework for styling and any JavaScript framework for UI interactivity.

## Pre-requisite knowledge

*Don't be intimidated by this section. By the time you go through the [Application components](https://volfpeter.github.io/holm/application-components) document and the [Quick start guide](https://volfpeter.github.io/holm/guides/quick-start-guide), you will have a very good intuition of how to use `holm`.*

To get started, all you need is a *basic* understanding of:

- [FastAPI](https://fastapi.tiangolo.com/tutorial/): the underlying web framework.
- [htmy](https://volfpeter.github.io/htmy/): the used component / templating and rendering library.
- HTML and CSS fundamentals.

Familiarity with [FastHX](https://volfpeter.github.io/fasthx/) (the rendering layer between `htmy` and `FastAPI`), and especially its `htmy` integration is useful, but not necessary, unless you are building an HTMX application.

It is recommended to use [HTMX](https://htmx.org/), if for nothing else, then to avoid hard page loads on navigation. [hx-boost](https://htmx.org/attributes/hx-boost/) (or navigation with `hx-get`) offers the same benefits as the `Link` component in Next.js.

## Installation

The package is available on PyPI and can be installed with:

```bash
pip install holm
```

Supported operating systems:

- Linux
- macOS
- Windows: WSL only (native support may arrive in the future)

## Support

Consider supporting the development and maintenance of the project through [sponsoring](https://buymeacoffee.com/volfpeter), or reach out for [consulting](https://www.volfp.com/contact?subject=Consulting%20-%20holm) so you can get the most out of the library.

## Application structure

Similarly to Next.js, `holm` is built around the concept of file-system based routing. This essentially means that your code structure is automatically mapped to a matching API:

- You do not need to manually define routes, every [application component](https://volfpeter.github.io/holm/application-components) is automatically discovered and registered in the application.
- You do not need to manually wrap pages in their layouts, it is automatically done based on your application's code structure.

You can find all the necessary details on the [Application components](https://volfpeter.github.io/holm/application-components) page, and the [Quick start guide](https://volfpeter.github.io/holm/guides/quick-start-guide) can walk you through the process of creating your first application. The two are complementary documents, reading both is strongly recommended.

HTML rendering is also fully automated, in the vast majority of cases you do not need to concern yourself with that (the only exceptions are HTML APIs, more on that in the [Rendering APIs with HTMX](https://volfpeter.github.io/holm/guides/rendering-apis-with-htmx) guide).

All you need to do is follow these simple rules:

- You must initialize your application instance using `holm.App()`. It optionally accepts a base `FastAPI` application and a `fasthx.htmy.HTMY` instance that handles HTML rendering.
- `holm.App()` must be called directly within a module in your root application package to make automatic application discovery work.

## Examples

If you prefer to learn through examples, the [Quick start guide](https://volfpeter.github.io/holm/guides/quick-start-guide) is the best place to start.

To learn about creating rendering APIs and adding HTMX to your application, you should have a look at the [Rendering APIs with HTMX](https://volfpeter.github.io/holm/guides/rendering-apis-with-htmx) guide.

The [Custom applications](https://volfpeter.github.io/holm/guides/custom-applications) guide shows you how to customize the FastAPI application instance as well as HTML rendering.

For error handling examples, you should check out the [Error Handling](https://volfpeter.github.io/holm/guides/error-handling) guide.

You can discover even more features by exploring the [test application](https://github.com/volfpeter/holm/tree/main/test_app) of the project.

If you are looking for the simplest possible application you can create, then can find it in the [examples/minimal](https://github.com/volfpeter/holm/tree/main/examples/minimal) directory of the repository.

## Security

At the moment, the library **does not** provide security features like automatic **CSRF prevention** out of the box. A custom form component and a corresponding middleware may be added to the library later, but of course 3rd party implementations are very welcome! Alternative solutions include JavaScript, but the library aims to remain unopinionated, especially on the client front. If you use HTMX, you should check out their [CSRF prevention](https://htmx.org/docs/#csrf-prevention) recommendation, just keep in mind that the `<body>` tag is not swapped for boosted requests.

Also, do not forget about **XSS prevention**, when rendering untrusted data with custom components!

## AI assistance

The library and all its dependencies are registered at [Context7](https://context7.com/volfpeter).

To get good AI assistance, all you need to do is register the Context7 MCP server in your coding tool and tell the agent to use it.

If you are starting a new project, you can additionally point the agent at one of the example applications in the [repository](https://github.com/volfpeter/holm). With all this context and detailed instructions of the project you want to build, it will get you started quickly.

Because of the similarity with Next.js and React, and the standard use of FastAPI and other dependencies, you can expect good results, both for vibe coding or inline completion.

## Technical notes

### Performance

Automatic application discovery and route registration takes only marginally more time compared to manual route registration. The performance difference during startup is unnoticeable.

When it comes to serving requests, there are two cases: standard JSON APIs and web applications.

For JSON APIs, the performance overhead is zero. In this case you are only using the application discovery feature of `holm`.

When building web applications, performance should be compared to an application that does all the rendering manually in routes, using `htmy`. In this case, a `holm` application will typically need to resolve a couple of additional dependencies, but because of the efficiency of FastAPI's dependency resolution mechanism, the performance impact is still unnoticeable.

### Templating language support

While certain features in `holm` rely heavily on the capabilities of `htmy` (for example its context and async support), you can still use other DSLs or templating languages (for example Jinja) in your application if you would like to. All you need to do is write a simple wrapper `htmy` component that internally offloads rendering to your framework of choice. You can find out more about this in the [htmy documentation](https://volfpeter.github.io/htmy/#compatibility-and-performance).

## Development

Development setup:

- `uv` for project and dependency management.
- `poethepoet` for running tasks. Run `uv run poe` to see all available tasks.
- `mypy` for static code analysis.
- `ruff` is used for formatting and linting.
- `pytest` for testing.
- `mkdocs-material` and `mkdocstrings` for documentation.

Tests are located in the `tests` directory and they use the application defined in the `test_app` package (through a `TestClient`). This setup makes it possible to run `test_app` outside of tests, which is useful for debugging.

You can run all tests with `uv run poe test`. You can separately start the test application with `uv run poe test-app`.

## Contributing

We welcome contributions from the community to help improve the project! Whether you're an experienced developer or just starting out, there are many ways you can contribute:

- **Discuss**: Join our [Discussion Board](https://github.com/volfpeter/holm/discussions) to ask questions, share ideas, provide feedback, and engage with the community.
- **Document**: Help improve the documentation by fixing typos, adding examples, and updating guides to make it easier for others to use the project.
- **Develop**: Prototype requested features or pick up issues from the issue tracker.
- **Test**: Write tests to improve coverage and reliability.

## Comparison with other frameworks

### Frameworks with JavaScript dependencies

The most prominent frameworks in this category are Reflex and NiceGUI. They both provide a Python-first web development experience while using complex JavaScript frameworks under the hood for constructing user interfaces (namely React and Vue.js). They take care of state management and synchronization (using WebSockets), seamlessly connecting the JavaScript frontend and the Python backend. In exchange for this convenience comes complexity and heavy reliance on the ever-changing JavaScript ecosystem.

`holm` comes with no JavaScript dependencies, but that doesn't mean you can't use JavaScript to add frontend interactivity. In fact, it comes with first class [HTMX](https://htmx.org/) support and naturally works with frameworks like [Alpine.js](https://alpinejs.dev/). Web component frameworks like [lit](https://lit.dev/), and even [React](https://react.dev/learn/add-react-to-an-existing-project#using-react-for-a-part-of-your-existing-page) application segments can also be integrated, just like into any server rendered page.

### Pure server-side rendering frameworks

This category includes frameworks like FastHTML or Ludic, and this is where `holm` belongs as well, but it has some key differentiators.

First, `holm` brings the Next.js developer experience to Python with file-system based routing, automatic layout composition, and dynamic page metadata creation, and more. Thanks to `htmy`, it supports async code throughout the stack, even in components, and it also solves the prop drilling problem. While being built with `htmy`, it is easy to integrate with other templating libraries, like `Jinja` or `htpy`. And it provides all these features using standard, simple FastAPI patterns.

## License

The package is open-sourced under the conditions of the [MIT license](https://choosealicense.com/licenses/mit/).
