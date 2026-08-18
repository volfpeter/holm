from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    css_file: str = "app.css"
    js_file: str = "app.js"


settings = Settings()
