from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    css_file: str = "app.css"
    js_file: str = "app.js"


settings = Settings()
