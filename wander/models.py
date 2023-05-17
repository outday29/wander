import argparse
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, validator

INVALID_SYMBOLS = ["!", "`", "-"]


class Plugin(BaseModel, ABC):
    plugin_name: str
    plugin_description: Optional[str] = None
    parser: argparse.ArgumentParser

    @validator("plugin_name")
    def validate_name(cls, value: str):
        for i in INVALID_SYMBOLS:
            if i in value:
                raise ValueError(f"Plugin name contains invalid symbol {i}")

        return value

    @abstractmethod
    async def run(self, args: Dict[str, Any], content: str):
        # We will always assume async run
        raise NotImplementedError

    def parse_args(self, tokenized: List[str]) -> Dict[str, Any]:
        args = self.parser.parse_args(tokenized)
        args = self.namespace_to_dict(args)
        return args

    def namespace_to_dict(self, namespace):
        return {
            k: self.namespace_to_dict(v) if isinstance(v, argparse.Namespace) else v
            for k, v in vars(namespace).items()
        }

    class Config:
        arbitrary_types_allowed = True


class Task(BaseModel, ABC):
    plugin_name: str
    args: List[str]
    content: str
