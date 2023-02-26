from fastapi import FastAPI
from routers import blockchains

app = FastAPI()

# Routers
app.include_router(blockchains.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
