import uvicorn
from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from routers import cars, web, auth
from routers.cars import BadTripException

app = FastAPI(title="Car Sharing")
app.include_router(cars.router)
app.include_router(web.router)
app.include_router(auth.router)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def welcome():
    return {'message': "Welcome to the Car Sharing service!"}


@app.exception_handler(BadTripException)
async def unicorn_exception_handler(request: Request, exc: BadTripException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip : " + exc.args[0]},
    )


# @app.middleware("http")
# async def add_cars_cookie(request: Request, call_next):
#     response = await call_next(request)
#     response.set_cookie(key="cars_cookie", value="you_visited_carsharing_app")
#     return response


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
