from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from routing.auth_router import router as auth_router
from routing.posting_router import router as posting_router
from database.session import Base, session,engine
from middlewares.JwtMiddleware import JwtMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from config import secret_key
import logging
import uvicorn
import jwt



denied = ("/api/post")

logging.basicConfig(filename="new_log.log", format="%(asctime)s %(message)s", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def app() -> FastAPI:
    app = FastAPI(root_path='/api')
    app.include_router(auth_router)
    app.include_router(posting_router)    
    app.add_middleware(GZipMiddleware)
    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(engine)
        
    @app.on_event('shutdown')
    def shutdown():
        session.close()
    
    @app.middleware("http")
    def JWTMiddleware(request: Request, call_next):
        if request.url.path.startswith(denied):
            try:
                cookie = str(request.cookies.get("jwt"))
                if cookie == None:
                    raise HTTPException(status_code=401, detail="Unauthorized")
                username = jwt.decode(cookie.encode(), secret_key, algorithms="HS256")['username']
                request.state.user = username
            except jwt.PyJwtError:
                raise HTTPException(status_code=401,detail="Unauthorized")
        response = call_next(request)
        return response

    
    @app.exception_handler(HTTPException)
    def httpexception_handler(exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={'message': exc.detail}) 
    
    return app

app = app()

if __name__=="__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
