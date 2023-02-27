from fastapi import APIRouter, HTTPException, status
from db.models.task import TaskData, TaskDB
from db.schemas.task import task_schema, tasks_schema
from db.client import db_client
from hashlib import sha256
from datetime import datetime

router = APIRouter(prefix="/tasks",
                   tags=["tasks"],
                   responses={status.HTTP_404_NOT_FOUND: {"error": "Not found"}})


# -------------------------------------------- CRUD ---------------------------------------------------------------#
@router.get("/", response_model=list[TaskDB])
async def tasks():
    task_list = get_tasks_list()

    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks have been created")
    else:
        valid_tasks_chain = chain_validation(task_list)
        if valid_tasks_chain:
            return task_list
        else:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                                detail={"error": f"valid_chain={valid_tasks_chain}"}
                                )


@router.post("/task", response_model=TaskDB, status_code=status.HTTP_201_CREATED)
async def task(task: TaskData):
    task_dict = create_new_task(task)

    db_client.tasks.insert_one(task_dict)

    tasks_list = get_tasks_list()

    valid_tasks_chain = chain_validation(tasks_list)

    if valid_tasks_chain:

        new_task = task_schema(db_client.tasks.find_one({"id_hash": task_dict["id_hash"]}))
        return TaskDB(**new_task)

    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail={"error": f"valid_chain={valid_tasks_chain}"}
                            )


@router.put("/", response_model=list[TaskDB], status_code=status.HTTP_201_CREATED)
async def tasks(tasks_list: list[TaskDB]):
    valid_tasks_chain = chain_validation(tasks_list)

    if not valid_tasks_chain:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail={"error": f"valid_chain={valid_tasks_chain}"}
                            )
    else:
        if get_tasks_list():
            db_client.tasks.drop()

        for task in tasks_list:
            db_client.tasks.insert_one(dict(task))

        return get_tasks_list()


# ----------------------------------------- Functions ------------------------------------------------------------#
def create_new_task(task: TaskData):
    new_db_task = TaskDB(data=task.data)
    new_db_task.timestamp = datetime.now()
    new_db_task.last_hash = search_last_hash()
    new_db_task.id_hash = create_hash(new_db_task)
    new_db_task.completed = False

    return dict(new_db_task)


def get_tasks_list():
    task_list = tasks_schema(db_client.tasks.find())
    return task_list


def search_last_hash():
    task_list = get_tasks_list()

    if not task_list:
        return ""
    else:
        last_task = task_list[len(task_list) - 1]
        return last_task["id_hash"]


def create_hash(task: TaskDB):
    timestamp = str(task.timestamp)
    data_string = timestamp + task.last_hash + task.data

    hash = sha256(data_string.encode()).hexdigest()
    return str(hash)


def chain_validation(tasks: list):
    valid_chain = True

    for task in range(1, len(tasks)):
        actual_task = dict(tasks[task])
        last_task = dict(tasks[task - 1])
        if actual_task["last_hash"] != last_task["id_hash"]:
            valid_chain = False
            return valid_chain

    return valid_chain
