from pathlib import Path


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        text = f.read()
        return text


def write_file(filepath: str, content: str) -> None:
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, "w") as f:
        f.write(content)
