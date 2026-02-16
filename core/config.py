from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    admin_email: str = "example@admin.com"
    
    DATABASE_URL_ONE: str = 'postgresql+asyncpg://postgres:password@localhost:5432/shopdb'
    DATABASE_URL_TWO: str = 'postgresql+psycopg2://postgres:password@localhost:5432/shopdb'
    DATABASE_PASSWORD: str = 'PostgreSQL.003'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = 'shopdb'
    DATABASE_USER: str = 'postgres'