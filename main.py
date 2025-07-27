from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from routing.auth_router import router as auth_router
from routing.posting_router import router as posting_router
from database.session import Base, session,engine
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from config import secret_key
import logging
import uvicorn
import jwt



denied = ("/api/post")

logging.basicConfig(filename="server_log.log", format="%(asctime)s %(message)s", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def app() -> FastAPI:
    app = FastAPI(root_path='/api')
    app.include_router(auth_router)
    app.include_router(posting_router)    

    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(engine)
        
    @app.on_event('shutdown')
    def shutdown():
        session.close()

    # works if some exception raised, outputs it to client
    @app.exception_handler(HTTPException)
    def exception_handler(exc: HTTPException):
        return exc(status_code=exc.status_code, detail=exc.detail)

    @app.middleware("http")
    def authentication_middleware(request: Request, call_next):
        
        """
        checks if url path not starts with route that require authentication
        if path not in denied, just send response, otherwise continue

        jwt/except block:
        first 'if' pulls cookie and in the same time checks if it isnt empty
        if it empty, raises HTTPException with code 401
        when cookie is not empty, this cookie decodes, result gives to username.
        if secret key of this jwt is invalid, works 'except' block and raises HTTPException error with code 401
        or, if all great, request.state.user gets username and middleware returns a response.
        """

        if not request.url.path.startswith(denied):
           return call_next(request)

        try:
            cookie = request.cookies.get("jwt")
            if cookie == "":
                raise HTTPException(status_code=401, detail="Unauthorized")
            username = jwt.decode(cookie.encode(), secret_key, algorithms="HS256")['username']
            request.state.user = username
            return call_next(request)
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Validation error!")
    return app

app = app()

if __name__=="__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
