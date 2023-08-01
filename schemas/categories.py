import pydantic

import uuid

class Category(pydantic.BaseModel):
    id: uuid.UUID
    projects: list[uuid.UUID]
    title: str
    color: str


class Project(pydantic.BaseModel):
    id: uuid.UUID
    tasks: list[uuid.UUID]
    title: str


class Task(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    urgent_color: str
    author: str
    executor: str
    comment: str
    date: str
    status: str