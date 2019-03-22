import pytest

POSTS_ENDPOINT = "/posts"
ONE_POST_ENDPOINT = "/posts/{}"
LIKE_POST_ENDPOINT = "/posts/{}/likes"


@pytest.fixture(scope="session")
def test_post_data():
    post_data = {"title": "The best test post",
                 "content": "This is the content of the best test post you ever saw."}
    return post_data


@pytest.yield_fixture
def post_id(client, test_post_data, access_token):
    '''Creates the post with test_post_data. Yields the post. Deletes the post'''
    headers = {"Authorization": "Bearer " + access_token}
    resp = client.post(POSTS_ENDPOINT, headers=headers, data=test_post_data)
    assert resp.status_code == 200
    post_id = resp.json["post"]["id"]
    yield post_id
    resp = client.delete(ONE_POST_ENDPOINT.format(post_id), headers=headers)


class TestPosts:
    def test_get_one(self, client, post_id):
        '''Test getting one post by id'''
        resp = client.get(ONE_POST_ENDPOINT.format(post_id))
        assert resp.status_code == 200

class TestLike:
    def test_toggle_like(self, client, access_token, post_id):
        '''Like and unlike one post'''
        headers = {"Authorization": "Bearer " + access_token}
        resp = client.put(LIKE_POST_ENDPOINT.format(post_id), headers=headers)
        assert resp.status_code == 200
        resp = client.delete(LIKE_POST_ENDPOINT.format(post_id), headers=headers)

    def test_nonexistent_post(self, client, access_token):
        '''Like abent post'''
        headers = {"Authorization": "Bearer " + access_token}
        resp = client.put(LIKE_POST_ENDPOINT.format(99999999999), headers=headers)
        assert resp.status_code == 404
