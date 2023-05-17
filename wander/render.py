import asyncio
import re
from typing import List

from pydantic import BaseModel

from .models import Plugin, Task

REGEX_PATTERN = r"```!(.*?)[\r\n](.*?)```"


class Renderer(BaseModel):
    plugins: List[Plugin]

    def render(self, text: str) -> str:
        task_list = self.get_task_list(text)
        output_list = asyncio.run(self.execute_task_list(task_list))
        return self.replace_output(text, output_list)

    def replace_output(self, text: str, output_list: str) -> str:
        index = -1

        def replace_block(match):
            nonlocal index
            index += 1
            return output_list[index]

        return re.sub(re.compile(REGEX_PATTERN, re.DOTALL), replace_block, text)

    def get_task_list(self, text: str) -> List[Task]:
        matches = re.findall(REGEX_PATTERN, text, re.DOTALL)
        # Create task from match
        task_list = []
        for i in matches:
            tokenized = i[0].strip().split()
            content = i[1]
            plugin_name = tokenized[0]
            args = tokenized[1:]
            task_list.append(Task(plugin_name=plugin_name, args=args, content=content))
        return task_list

    async def execute_task_list(self, task_list: List[Task]):
        return await asyncio.gather(*[self.execute_task(task) for task in task_list])

    async def execute_task(self, task: Task):
        for plugin in self.plugins:
            if plugin.plugin_name == task.plugin_name:
                args = plugin.parse_args(task.args)
                return await plugin.run(args=args, content=task.content)
        raise ValueError(f"Plugin with plugin_name {task.plugin_name} not found.")
