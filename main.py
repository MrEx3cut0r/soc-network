from fastapi import FastAPI
import uvicorn


def app() -> FastAPI:
    app = FastAPI()
    return app

app = app()

if __name__=="__main__":
    uvicorn.run('main:app', reload=True)