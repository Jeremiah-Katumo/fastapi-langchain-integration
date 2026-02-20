import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST: str = os.getenv("DATABASE_HOST")
DATABASE_PORT: int = os.getenv("DATABASE_PORT")
DATABASE_NAME: str = os.getenv("DATABASE_NAME")
DATABASE_USER: str = os.getenv("DATABASE_USER")
DATABSE_DRIVER: str = os.getenv("DATABSE_DRIVER")

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    admin_email: str = "example@admin.com"
    
    DATABASE_URL_ONE: str = f'{DATABSE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    DATABASE_URL_TWO: str = f'{'postgresql+psycopg2'}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    
    class Config:
        env_file = "env"
        
settings = Settings()