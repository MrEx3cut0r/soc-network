from fastapi import APIRouter, Depends, Response
from datetime import datetime, timedelta
from services.user_service import ret_user_service
from dtos.user import user as user_dto
import jwt
router = APIRouter()

@router.post('/login')
async def login(username, password, response: Response, service: ret_user_service = Depends()):
    if await service.validate_password(username, password):
        await response.set_cookie(key="access_jwt", value=jwt.encode({'username': username}), expires=datetime.now()+timedelta(hours=7))
        return True
    return False

@router.post('/register')
async def register(username, email, password, service: ret_user_service = Depends()):
    user = user_dto(username=username, email=email, password=password)
    if user:
        return 'user already exists'
    return await service.create_user(user)

@router.post('/logout')
async def logout(response: Response):
    return await response.delete_cookie("access_jwt")

