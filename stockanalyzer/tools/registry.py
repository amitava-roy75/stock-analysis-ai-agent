from typing import Dict
from tools.base_tool import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    def register(self, tool: BaseTool):
        self._tools[tool.name]=tool
    def get(self,name:str):
        return self._tools.get(name)
    def list_tools(self):
        return list(self._tools.keys())

registry=ToolRegistry()
