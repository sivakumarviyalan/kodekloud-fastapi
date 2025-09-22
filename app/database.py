from sqlmodel import create_engine, Session
from .config import settings

engine = create_engine(
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

def get_session():
    with Session(engine) as session:
        yield session
