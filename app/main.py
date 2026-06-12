from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import redis
import os

app = FastAPI(title="Task Manager API", version="1.0.0")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

tasks = {}
task_counter = 0


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "task-manager"}


@app.get("/tasks")
def get_tasks():
    return {"tasks": list(tasks.values())}


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global task_counter
    task_counter += 1
    task_id = task_counter
    tasks[task_id] = {"id": task_id, **task.model_dump()}
    redis_client.set(f"task:{task_id}", task.title)
    return tasks[task_id]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    redis_client.delete(f"task:{task_id}")
    del tasks[task_id]
    return {"message": "Task deleted"}
