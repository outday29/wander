import argparse
import subprocess
from typing import Any, Dict

from ..models import Plugin

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "-e", "--output-error", action="store_true", help="Allow error output"
)


class ShellPlugin(Plugin):
    plugin_name: str = "shell"
    plugin_description: str = "Run shell command and return output"
    parser: argparse.ArgumentParser = PARSER

    async def run(self, args: Dict[str, Any], content: str) -> str:
        try:
            output = (
                subprocess.check_output(content, shell=True, stderr=subprocess.STDOUT)
                .decode()
                .strip()
            )
            return output
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode().strip()
            if args["output_error"]:
                return f"Error executing command:\n{content}\n{error_output}"
            else:
                raise RuntimeError(
                    f"Error executing command:\n{content}\n{error_output}"
                )
