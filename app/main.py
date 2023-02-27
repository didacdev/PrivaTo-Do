from fastapi import FastAPI
from routers import tasks

# ejecutar MacOS: python3 -m uvicorn app.main:app --reload
# ejecutar Windows: C:\Users\Diego\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\uvicorn.exe app.main:app --reload

app = FastAPI()

# Routers
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

