import pytest
from app import schemas

@pytest.fixture()
def test_vote(test_user, session, test_posts):
    new_vote = schemas.Votes(user_id=test_user['id'], post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()
    return new_vote

def test_vote_on_post_success(auth_client, test_user, test_posts):
    res = auth_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post_conflict(auth_client, test_posts, test_vote):
    res = auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_vote_on_post_not_found(auth_client, test_posts):
    res = auth_client.post("/vote/", json={"post_id": 99999, "dir": 1})
    assert res.status_code == 404

def test_delete_vote_success(auth_client, test_posts, test_vote):
    res = auth_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_not_found(auth_client, test_posts):
    res = auth_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401