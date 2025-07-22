from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from routing.auth_router import router as auth_router
from routing.posting_router import router as posting_router
from database.session import Base, session,engine
from middlewares.JwtMiddleware import JwtMiddleware
import uvicorn

jwtmiddleware = JwtMiddleware()

def app() -> FastAPI:
    app = FastAPI(root_path='/api')
    app.include_router(auth_router)
    app.include_router(posting_router)
    app.add_middleware(BaseHTTPMiddleware, dispatch=jwtmiddleware)
    
    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(engine)
    @app.on_event('shutdown')
    def shutdown():
        session.close()
        
    return app

app = app()

if __name__=="__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)