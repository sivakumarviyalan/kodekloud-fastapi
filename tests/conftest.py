from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
import pytest
from alembic import command

from app.main import app
from app import schemas
from app.config import settings
from app.database import get_session
from app.oauth2 import create_access_token

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

@pytest.fixture
def test_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "password123"
    return new_user

@pytest.fixture
def test_user2(client):
    res = client.post("/users/", json={"email": "siva@gmail.com", "password": "password123"})

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "password123"
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({
        "user_id": test_user['id']
    })

@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return schemas.Posts(**post)

    post_models = list(map(create_post_model, posts_data))
    session.add_all(post_models)
    session.commit()
    posts = session.query(schemas.Posts).all()
    return posts