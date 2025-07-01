from fastapi import FastAPI
from routing.auth_router import router as auth_router
from database.session import Base, session,engine
import uvicorn


def app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_router)

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