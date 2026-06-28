from pydantic import BaseModel


class Task(BaseModel):

    tool: str

    input: str