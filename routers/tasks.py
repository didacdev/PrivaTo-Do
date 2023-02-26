from fastapi import APIRouter, HTTPException, status
from db.models.task import Task
from db.schemas.task import task_schema, tasks_schema
from db.client import db_client
from hashlib import sha256
from datetime import datetime

router = APIRouter(prefix="/tasks",
                   tags=["tasks"],
                   responses={status.HTTP_404_NOT_FOUND: {"error": "Not found"}})


@router.get("/", response_model=list[Task])
async def tasks():
    task_list = tasks_schema(db_client.tasks.find())

    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks have been created")
    else:
        return task_list


@router.post("/task", response_model=Task, status_code=status.HTTP_201_CREATED)
async def task(task: Task):
    task_dict = create_new_task(task)

    db_client.tasks.insert_one(task_dict)

    new_task = task_schema(db_client.tasks.find_one({"id_hash": task_dict["id_hash"]}))

    return Task(**new_task)


def create_new_task(task: Task):
    task.timestamp = datetime.now()
    task.last_hash = search_last_hash()
    task.id_hash = create_hash(task)
    task.completed = False

    return dict(task)


def search_last_hash():
    task_list = tasks_schema(db_client.tasks.find())

    if not task_list:
        return ""
    else:
        last_task = task_list[len(task_list) - 1]
        return last_task["id_hash"]


def create_hash(task: Task):
    timestamp = str(task.timestamp)
    data_string = timestamp + task.last_hash + task.data

    hash = sha256(data_string.encode()).hexdigest()
    return str(hash)
