from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_content_length: int = 200000
    stanza_models_dir: str = "stanza_resources"

settings = Settings()