from fastapi import FastAPI
from routers import tasks

# ejecutar MacOS: python3 -m uvicorn app.main:app --reload
# ejecutar Windows: C:\Users\Diego\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\uvicorn.exe app.main:app --reload

description = """
PrivaTo-Do is a **TODO list** and **note-taking**. The main difference of this app is that the tasks are
stored in a [blockchain](https://builtin.com/blockchain) that creates a history with all the changes and modifications
of the different notes/tasks.
Check the Github repository [didacdev](https://github.com/didacdev).

## Tasks

* You can send request to the API to **add** or **mark as completed** any task.
* It is also possible to replace de present blockchain 
* Finally, you can just get the blockchain to read the task data

"""

app = FastAPI(
    title="PrivaTo-Do",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Diego Sánchez Escribano",
        "url": "https://didacdev.super.site/",
        "email": "diego.sanchez.escribano@pm.me",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/",
    },
    docs_url="/"
)

# Routers
app.include_router(tasks.router)

