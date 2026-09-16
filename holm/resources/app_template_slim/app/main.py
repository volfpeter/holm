from components.theme_switcher import theme_switcher
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from holm import App, OriginCheckMiddleware

from .head import head

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(OriginCheckMiddleware)
# TODO: enable trusted hosts before deploying to harden the origin check.
# from starlette.middleware.trustedhost import TrustedHostMiddleware
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "example.com"])

app.mount("/static", StaticFiles(directory="static"), name="static")

App(
    app=app,
    layout_slots={"head": head, "theme_switcher": theme_switcher()},
)
