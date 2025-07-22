from fastapi import Request, HTTPException


denied = ['post']


class JwtMiddleware():
    def __call__(self, request: Request, call_next):
        if str(request.url.path) in denied:
            if request.get.cookie("jwt") == "":
                raise HTTPException(status_code=401, detail="Unauthorized")
        response = call_next(request)
        return response

