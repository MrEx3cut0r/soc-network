from fastapi import APIRouter, Depends, Response
from datetime import datetime, timedelta, timezone
from services.user_service import ret_user_service
from dtos.user import user as user_dto
from config import secret_key
from services.subscribing_service import ret_subscribing_service
import jwt
router = APIRouter(prefix="/auth")

@router.post('/login')
def login(username: str, password: str, response: Response, service: ret_user_service = Depends()):
    if service.validate_password(username, password):
        response.set_cookie(key="jwt", value=jwt.encode({'username': username}, secret_key, 'HS256'), expires=datetime.now(timezone.utc)+timedelta(hours=7), httponly=True)
        return True
    return False

@router.post('/register')
def register(username: str, email: str, password: str, user_service: ret_user_service = Depends(), sub_service: ret_subscribing_service = Depends()):
    user = user_service.search_user(username)
    if user:
        return 'user already exists'
    new_user = user_dto(username=username, email=email, password=password)
    sub_service.create_profile(new_user.username)
    return user_service.create_user(new_user)

@router.post('/logout')
def logout(response: Response):
    return response.delete_cookie("jwt")

