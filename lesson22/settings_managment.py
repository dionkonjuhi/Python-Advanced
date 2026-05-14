from pydantic import BaseSettings
from pydeck import settings


class Settings(BaseSettings):
    app_name: str
    admin_email: str
    item_per_user: int = 50

settings = Settings()