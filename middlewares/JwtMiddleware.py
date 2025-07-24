from fastapi import Request, HTTPException
import jwt
from config import secret_key

denied = ['post']


class JwtMiddleware():
    def __call__(self, request: Request, call_next):
        exception = HTTPException(status_code=401, detail="Unauthorized")
        if str(request.url.path) in denied:
            """
            try:
                cookie = request.cookies.get("jwt")
                jwt.decode(cookie, secret_key, algorithm="HS256")
                if cookie == "":
                    raise exception
            
            except:
                raise exception
           
                
            """
            print("in denied")
        response = call_next(request)
        return response

