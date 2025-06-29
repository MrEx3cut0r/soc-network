from fastapi import APIRouter, Request
from datetime import datetime, timezone, timedelta

router = APIRouter()

@router.post('/login')
def login(username, password, request: Request):
    pass

@router.post('/register')
def register(username, email, password):
    pass

@router.post('/logout')
def logout():
    pass

