import pytest

POSTS_ENDPOINT = "/posts"
ONE_POST_ENDPOINT = "/posts/{}"


@pytest.fixture(scope="session")
def test_post_data():
    post_data = {"title": "The best test post",
                 "content": "This is the content of the best test post you ever saw."}
    return post_data


# @pytest.yield_fixture(scope="function")
# def headers(access_token):

class TestPosts:
    def test_success_creation(self, client, test_post_data, access_token):
        headers = {"Authorization": "Bearer " + access_token}
        resp = client.post(POSTS_ENDPOINT,
                           headers=headers,
                           data=test_post_data)
        assert resp.status_code == 200
        post_id = resp.json["post"]["id"]
        resp = client.delete(ONE_POST_ENDPOINT.format(post_id),
                             headers=headers)
