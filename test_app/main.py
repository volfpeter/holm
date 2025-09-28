from fastapi import FastAPI
from fasthx.htmy import HTMY

from holm import App

app = FastAPI()
htmy = HTMY(
    request_processors=[
        # Add a request processor that inserts an "is_htmx_request" key
        # into htmy rendering contexts, making this information available
        # to htmy components as `context["is_htmx_request"]`.
        lambda request: {"is_htmx_request": request.headers.get("HX-Request") == "true"}
    ]
)


@app.get("/health-check")
def health_check() -> dict[str, str]:
    """Health check route registered directly on the FastAPI application."""
    return {"status": "ok"}


# If holm.App() receives a FastAPI application instance, then it does its job and
# returns the same object. This means you don't need to keep a separate reference
# to the returned value, the already existing app variable is enough.
App(app=app, htmy=htmy)
