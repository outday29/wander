from argparse import ArgumentParser
from typing import Any, Dict
from wander.models import Plugin

class ClipboardPlugin(Plugin):
    plugin_name: str = "clip"
    plugin_description: str = "Access text from clipboard"
    parser: ArgumentParser = ArgumentParser()

    async def run(self, args: Dict[str, Any], content: str) -> str:
        from tkinter import Tk
        return Tk().clipboard_get()