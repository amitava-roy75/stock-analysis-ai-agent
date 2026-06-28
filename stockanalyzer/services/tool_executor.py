import asyncio
from tools.registry import registry

class ToolExecutor:
    async def execute_tool(self,tool_name:str,input_data:str):
        tool=registry.get(tool_name)
        if tool is None:
            return {"tool":tool_name,"status":"FAILED","message":"Unknown Tool"}
        result=await tool.execute(input_data)
        return {"tool":tool_name,"status":"SUCCESS","result":result}

    async def execute_parallel(self,tasks):
        return await asyncio.gather(*[
            self.execute_tool(t["tool"],t["input"]) for t in tasks
        ])

tool_executor=ToolExecutor()
