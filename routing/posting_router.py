from fastapi import APIRouter, Request, Depends
from services.posts_service import ret_post_service
from dtos.post import Post
import os
import jwt
import datetime

router = APIRouter(prefix="/post")


def extract_username(encoded: str) -> str:
    secret_key = str(os.getenv('secret_key'))
    return jwt.decode(encoded, secret_key, algorithms="HS256")['username']


@router.post("/create")
def create_post(text: str, request: Request, service: ret_post_service = Depends()):
    username = extract_username(str(request.cookies.get('jwt')))
    now = str("{:%d/%m/%Y}".format(datetime.datetime.now()))
    new_post = Post(username=username, text=text, when=now)
    return service.create(new_post)
    
@router.delete('/delete/{id}')
def delete_post(id: int, request: Request, service: ret_post_service = Depends()):
    username = extract_username(str(request.cookies.get('jwt')))
    post = service.findById(id)
    if post and post.username == username:
        return service.findById(id)
    return "Publication not found."