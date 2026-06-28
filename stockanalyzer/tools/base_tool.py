from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self)->str: ...
    @abstractmethod
    async def execute(self,input_data:str)->Any: ...
