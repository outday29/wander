from textwrap import dedent

import pytest

from wander import Renderer
from wander.plugins import ShellPlugin


@pytest.fixture
def example_valid_md():
    valid_1 = dedent(
        """\
    What is your message?
    ```!shell
    echo "Hello world"
    ```"""
    )
    valid_2 = dedent(
        """\
    Message 1
    ```!shell
    echo "Hello"
    ```
    Message 2
    ```!shell
    echo "World"
    ```"""
    )
    return [
        valid_1,
        valid_2,
    ]


@pytest.fixture
def example_invalid_md():
    invalid_1 = dedent(
        """\
    Invalid command
    ```!shella
    echo "hello"
    ```"""
    )
    return [invalid_1]


def test_valid_md(example_valid_md):
    renderer = Renderer(plugins=[ShellPlugin()])
    output_1 = renderer.render(example_valid_md[0])
    output_2 = renderer.render(example_valid_md[1])

    expected_1 = dedent(
        """\
    What is your message?
    Hello world"""
    )

    expected_2 = dedent(
        """\
    Message 1
    Hello
    Message 2
    World"""
    )

    assert output_1 == expected_1
    assert output_2 == expected_2


def test_invalid_md(example_invalid_md):
    with pytest.raises(ValueError):
        renderer = Renderer(plugins=[ShellPlugin()])
        renderer.render(example_invalid_md[0])
