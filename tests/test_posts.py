from app import schemas
import pytest

def test_get_all_posts(auth_client, test_posts):
    res = auth_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200  

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_found(auth_client, test_posts):
    res = auth_client.get(f"/posts/99999")
    assert res.status_code == 404

def test_get_one_post(auth_client, test_posts):
    res = auth_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json()[0])
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.title == test_posts[0].title
    assert post.Posts.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize(
    "title, content, published", [
        ("Awesome new title", "Awesome new content", True),
        ("favorite pizza", "i love pepperoni", True),
        ("tallest skyscrapers", "wahoo", True)
    ]
)
def test_create_post(auth_client, test_user, test_posts, title, content, published):
    res = auth_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Posts(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    assert res.status_code == 201

def test_create_post_default_published_true(auth_client, test_user, test_posts):
    res = auth_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    created_post = schemas.Posts(**res.json())
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    assert res.status_code == 201

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 401

def test_delete_post_success(auth_client, test_user, test_posts):
    res = auth_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_found(auth_client, test_user, test_posts):
    res = auth_client.delete(f"/posts/99999")
    assert res.status_code == 404

def test_delete_post_unauthorized_user(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_forbidden(auth_client, test_user, test_posts):
    res = auth_client.delete(
        f"/posts/{test_posts[3].id}"  # post created by test_user2
    )
    assert res.status_code == 403

def test_update_post_success(auth_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }
    res = auth_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Posts(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200

def test_update_post_not_found(auth_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = auth_client.put(f"/posts/99999", json=data)
    assert res.status_code == 404

def test_update_post_unauthorized_user(client, test_user, test_posts):
    data = {
        "title": "updated title", 
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_forbidden(auth_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = auth_client.put(f"/posts/{test_posts[3].id}", json=data)  # post created by test_user2
    assert res.status_code == 403
    