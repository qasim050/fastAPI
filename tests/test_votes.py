import pytest
import models

@pytest.fixture
def test_voted(session,test_create_user,test_posts):
    voted_post = models.Vote(user_id = test_create_user["id"], post_id =test_posts[3].id)
    session.add(voted_post)
    session.commit()

def test_vote(authorized_client,test_posts):
    res = authorized_client.post("/votes/",json = {"post_id":test_posts[3].id,"dir":1})
    assert res.status_code ==201


def test_voted_twise(authorized_client,test_posts,test_voted):
    res = authorized_client.post("/votes/",json = {"post_id":test_posts[3].id,"dir":1})
    assert res.status_code ==409

def test_delete_vote(authorized_client,test_posts,test_voted):
    res = authorized_client.post("/votes/",json = {"post_id":test_posts[3].id,"dir":0})
    assert res.status_code ==201
    
def test_delete_vote_non_exist(authorized_client,test_posts,test_voted):
    res = authorized_client.post("/votes/",json = {"post_id":test_posts[1].id,"dir":0})
    assert res.status_code ==404

def test_vote_non_exist(authorized_client,test_posts,test_voted):
    res = authorized_client.post("/votes/",json = {"post_id":80000,"dir":1})
    assert res.status_code ==404

def test_unauthorized_user_vote(client,test_posts,test_voted):
    res = client.post("/votes/",json = {"post_id":test_posts[1].id,"dir":1})
    assert res.status_code ==401
