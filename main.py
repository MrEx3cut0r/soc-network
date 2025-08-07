from fastapi import FastAPI, Request, HTTPException, Depends
from services.user_service import ret_user_service
from starlette.middleware.base import BaseHTTPMiddleware
from routing.auth_router import router as auth_router
from routing.posting_router import router as posting_router
from routing.user_router import router as user_router
from database.session import Base, session,engine
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from config import secret_key
import logging
import uvicorn
import jwt



denied = ("/api/post", "/api/users")

def app() -> FastAPI:
    app = FastAPI(root_path='/api')
    app.include_router(auth_router)
    app.include_router(posting_router)    
    app.include_router(user_router)

    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(engine)
        
    @app.on_event('shutdown')
    def shutdown():
        session.close()

    # works if some exception raised, outputs it to client
    @app.exception_handler(HTTPException)
    def exception_handler(exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, detail=exc.detail)

    @app.middleware("http")
    def JWTMiddleware(request: Request, call_next):
        service =  ret_user_service()
        if request.url.path.startswith(denied):
            try:
                cookie = request.cookies.get("jwt")
                if cookie == None:
                    raise jwt.pyJWTError
                username = jwt.decode(cookie.encode(), secret_key, algorithms="HS256")['username']
                if service.search_user(username) == False:
                    raise jwt.PyJWTError
                request.state.user = username
                return call_next(request)
            except jwt.PyJWTError:
                raise HTTPException(status_code=401, detail="Unauthorized")
        response = call_next(request)
        return response

    return app

app = app()

if __name__=="__main__":
    logging.basicConfig(filename="server_log.log", format="%(asctime)s %(message)s", filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler() 
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
