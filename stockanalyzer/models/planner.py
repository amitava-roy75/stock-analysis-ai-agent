from typing import List

from pydantic import BaseModel

from models.task import Task


class PlannerResult(BaseModel):

    intent: str

    company: str

    symbol: str = ""

    tasks: List[Task]