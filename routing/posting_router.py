from fastapi import APIRouter, Request, Depends
from services.posts_service import ret_post_service
from dtos.post import Post
from dtos.post import Post
from config import secret_key
from typing import Optional, List
import jwt
import datetime

router = APIRouter(prefix="/post")

@router.post("/create")
def create_post(text: str, request: Request, service: ret_post_service = Depends()) -> Optional[Post]:
    username = request.state.user
    now = str("{:%d/%m/%Y}".format(datetime.datetime.now()))
    new_post = Post(username=username, text=text, when=now)
    return service.create(new_post)
    
@router.delete('/{id}')
def delete_post(id: int, request: Request, service: ret_post_service = Depends()) -> Optional[Post] | str:
    username = request.state.user
    post = service.findById(id)
    if post and post.username == username:
        return service.findById(id)
    return "Publication not found."
    
@router.get('/me')
def get_my(request: Request, service: ret_post_service = Depends()) -> List[Post]:
    username = request.state.user
    my = service.findByUsername(username)
    return my
