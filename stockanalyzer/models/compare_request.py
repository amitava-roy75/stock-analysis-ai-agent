from typing import List

from pydantic import BaseModel


class CompareRequest(BaseModel):
    symbols: List[str]