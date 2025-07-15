import schemas
import pytest
def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate,res.json())
    posts = list(post_map)


    assert len(res.json()) == len(test_posts) 
    assert res.status_code == 200

def test_unauthorized_get_all_post(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_get_not_exist_post(authorized_client,test_posts):
    res = authorized_client.get("/posts/000")
    assert res.status_code == 404
    
def test_get_one_post(authorized_client,test_posts):
        res = authorized_client.get(f"/posts/{test_posts[0].id}")
        print(res.json())
        post = schemas.PostOut(**res.json())
        assert post.Post.id == test_posts[0].id
        
@pytest.mark.parametrize("title,content,published",[
    ("my title","my content",True),
    ("my title2","my content2",True),
    ("my title3","my content3",False)
])
def test_create_post(authorized_client,test_posts,test_create_user,title,content,published):
    res = authorized_client.post("/posts/",json ={"title":title,"content": content,"published":published})
    print(res.json())
    created_post = schemas.ReturnPost(**res.json())
    
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_create_user["id"]

def test_create_post_published_defult_true(authorized_client,test_posts,test_create_user):
    res = authorized_client.post("/posts/",json ={"title":"title","content": "content"})
    created_post = schemas.ReturnPost(**res.json())
    
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner.id == test_create_user["id"]
    
def test_unauthorized_create_all_post(client,test_posts):
    res = client.post("/posts/",json ={"title":"title","content": "content"})
    assert res.status_code == 401
    
def test_unauthorized_delete_post(client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client,test_posts):
    res = authorized_client.delete("/posts/00000")
    assert res.status_code == 404
    

def test_delete_others_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client,test_posts):
    data ={
        "title":"update title","content": "update content" ,"id": test_posts[0].id
    }    

    res = authorized_client.put(f"/posts/{test_posts[0].id}",json = data)
    assert res.status_code == 200
    update_post = schemas.ReturnPost(**res.json())
    assert update_post.title == data["title"]
    assert update_post.content == data["content"]
    assert update_post.id == data["id"]

def test_update_others_post(authorized_client,test_posts):
    
    data ={
        "title":"update title","content": "update content" ,"id": test_posts[3].id
    }    
    res = authorized_client.put(f"/posts/{test_posts[3].id}",json = data)
    assert res.status_code == 403
    
def test_unauthorized_user_updata_post(client,test_posts):
    data ={
        "title":"update title","content": "update content" ,"id": test_posts[0].id
    }    
    res = client.put(f"/posts/{test_posts[0].id}",json=data)
    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client,test_posts):
    data ={
        "title":"update title","content": "update content" ,"id": test_posts[0].id
    }    
    res = authorized_client.put("/posts/00000",json =data)
    assert res.status_code == 404
    
