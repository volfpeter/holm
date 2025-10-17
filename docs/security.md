# Security

While `holm` is built on top of the secure foundations of FastAPI and can take advantage of its entire ecosystem, it is still important to be mindful of common web vulnerabilities, especially Cross-Site Request Forgery (CSRF) and Cross-Site Scripting (XSS).

## XSS prevention

`holm` uses `htmy` under the hood, which performs XML/HTML escaping by default. You can find more information about this in the [htmy documentation](https://volfpeter.github.io/htmy/#xss-prevention).

## Cross-Site Request Forgery (CSRF) prevention

`holm` takes a similar approach to CSRF prevention as Next.js, relying on web security fundamentals and modern browser security features:

- **HTTP-only** cookies, which are not accessible from JavaScript.
- **Secure** cookies, which are only sent over HTTPS.
- `lax` or `strict` **SameSite** cookie policy.
- Cryptographically **signed** cookies to ensure data integrity and authenticity.
- Avoiding state-changing operations in HTTP **GET** requests.

Together, these offer reasonable protection against CSRF attacks.

`holm` encourages these practices for example through:

- reliance on the FastAPI ecosystem;
- the `handle_submit()` functionality in `page.py` modules for `POST` requests;
- the custom `APIRouter` support in `api.py` modules.

FastAPI middlewares that check the `Host`, `Origin`, and `Referer` headers can be used to add some additional security measures.

For even more security, you should use CSRF tokens. The exact implementation depends on your application's architecture and frontend framework (if any). If you are using HTMX, you should follow their [CSRF prevention recommendations](https://htmx.org/docs/#csrf-prevention).
