from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
import pytest
from alembic import command

from app.main import app
from app.config import settings
from app.database import get_session


# engine = create_engine(
#     f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# )

engine = create_engine(
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

@pytest.fixture()
def session():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db_session:
        yield db_session

@pytest.fixture()
def client(session):
    def override_get_session():
        yield session
    app.dependency_overrides[get_session] = override_get_session
    # command.upgrade("head")
    yield TestClient(app)
    # command.downgrade("base")