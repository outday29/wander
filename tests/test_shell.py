from textwrap import dedent

import pytest

from wander import Renderer
from wander.plugins import ShellPlugin


def test_error_flag():
    text_1 = dedent(
        """\
    This will give an error:
    ```!shell
    cat hello.txt
    ```"""
    )
    text_2 = dedent(
        """\
    This will not give an error:
    ```!shell -e
    cat hello.txt
    ```"""
    )
    renderer = Renderer(plugins=[ShellPlugin()])
    with pytest.raises(RuntimeError):
        renderer.render(text=text_1)

    output = renderer.render(text=text_2)
    expected = dedent(
        """\
    This will not give an error:
    Error executing command:
    cat hello.txt

    cat: hello.txt: No such file or directory"""
    )

    assert output == expected
