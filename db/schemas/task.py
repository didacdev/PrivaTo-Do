from db.models.task import TaskData

def task_schema(task) -> dict:
    return {"id_hash": task["id_hash"],
            "timestamp": task["timestamp"],
            "data": task["data"],
            "last_hash": task["last_hash"],
            "completed": task["completed"]}

def tasks_schema(tasks) -> list:
    return [task_schema(task) for task in tasks]

