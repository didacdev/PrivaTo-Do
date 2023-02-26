from fastapi import FastAPI
from routers import tasks

app = FastAPI()

# Routers
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
