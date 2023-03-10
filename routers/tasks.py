from fastapi import APIRouter, HTTPException, status
from db.models.task import TaskData, TaskDB
from db.schemas.task import task_schema, tasks_schema
from db.client import db_client
from hashlib import sha256
from datetime import datetime

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations with tasks."
    }
]

router = APIRouter(prefix="/tasks",
                   tags=["tasks"],
                   responses={status.HTTP_404_NOT_FOUND: {"error": "Not found"}})


# -------------------------------------------- CRUD ---------------------------------------------------------------#
@router.get("/", response_model=list[TaskDB])
async def tasks():
    """
    Returns a task list as a blockchain.
    """
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
    """
    Creates a new task with the completed field as False from the data written in the request body.
    """
    task_dict = create_task(task, False)

    return insert_task(task_dict)


@router.put("/task", response_model=TaskDB, status_code=status.HTTP_201_CREATED)
async def task(task: TaskDB):
    """
    Updates a task as completed. The task must be introduced in the request body with the completed field as True.
    """
    task_dict = create_task(task, True)

    return insert_task(task_dict)


@router.put("/", response_model=list[TaskDB], status_code=status.HTTP_201_CREATED)
async def tasks(tasks_list: list[TaskDB]):
    """
    Replaces the present blockchain with the one that is introduced in the request body.
    """
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
def create_task(task: TaskData, state: bool):
    """"
    Creates and returns a new task object from the fields data and completed
    """
    new_db_task = TaskDB(data=task.data)
    new_db_task.timestamp = datetime.now()
    new_db_task.last_hash = search_last_hash()
    new_db_task.id_hash = create_hash(new_db_task)
    new_db_task.completed = state

    return dict(new_db_task)


def create_hash(task: TaskDB):
    """
    Creates a new hash for the task block introduced as a param from de timestamp, data and last_hash fields
    :param task: task block to use in the function
    :return: a string with the new hash
    """
    timestamp = str(task.timestamp)
    data_string = timestamp + task.last_hash + task.data

    hash = sha256(data_string.encode()).hexdigest()
    return str(hash)


def get_tasks_list():
    task_list = tasks_schema(db_client.tasks.find())
    return task_list


def search_last_hash():
    """
    Looks for the id_hash of the last task that has been created
    :return: a string with the id_hash of the last task created
    """
    task_list = get_tasks_list()

    if not task_list:
        return ""
    else:
        last_task = task_list[len(task_list) - 1]
        return last_task["id_hash"]


def chain_validation(tasks: list):
    valid_chain = True
    first_task = dict(tasks[0])

    if first_task["last_hash"]:
        valid_chain = False
        return valid_chain

    for task in range(1, len(tasks)):
        actual_task = dict(tasks[task])
        last_task = dict(tasks[task - 1])
        if actual_task["last_hash"] != last_task["id_hash"]:
            valid_chain = False
            return valid_chain

    return valid_chain


def insert_task(task: dict):
    db_client.tasks.insert_one(task)

    tasks_list = get_tasks_list()

    valid_tasks_chain = chain_validation(tasks_list)

    if valid_tasks_chain:

        new_task = task_schema(db_client.tasks.find_one({"id_hash": task["id_hash"]}))
        return TaskDB(**new_task)

    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail={"error": f"valid_chain={valid_tasks_chain}"}
                            )
