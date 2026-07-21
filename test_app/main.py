from fastapi import FastAPI
from fasthx.htmy import HTMY

from holm import App

from .navbar import navbar

app = FastAPI()

htmy = HTMY()


@app.get("/health-check")
def health_check() -> dict[str, str]:
    """Health check route registered directly on the FastAPI application."""
    return {"status": "ok"}


# If holm.App() receives a FastAPI application instance, then it does its job and
# returns the same object. This means you don't need to keep a separate reference
# to the returned value, the already existing app variable is enough.
App(app=app, layout_slots={"navbar": navbar})
