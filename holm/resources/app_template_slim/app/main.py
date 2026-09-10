from components.theme_switcher import theme_switcher
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from holm import App

from .head import head

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

App(
    app=app,
    layout_slots={"head": head, "theme_switcher": theme_switcher()},
)
