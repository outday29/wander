# Wander

`wander` is a simple Python library that makes it easier to incorporate external data into LLM prompt.

## Installation

You can install `wander` with `pip`

```python
pip install wander
```

You need to have Python version of 3.10 or above to use this library.

## Usage

Assuming you have an markdown text with a special block `!shell`.

````python
text = """\
Today is:
```!shell
date
```
"""
````

Using `wander` to render it.

```python
from wander import Renderer
from wander.plugins import ShellPlugin

renderer = Renderer(plugins=[ShellPlugin])
renderer.render(text)
```

Output:
```
Today is:
Wed May 17 16:48:09 +08 2023
```


## Writing your own plugin

To write your own plugin, simply inherit the `Plugin` class and do the following:

- Specify `plugin_name` property. This will be the name of the directive used in your special block.
- Specify `parser` property, which is an `argparse.ArgumentParser` object to define what CLI-like arguments are accepted after the directive name
- Implement `run` async method. It must takes an `args` argument holding all the values of the command arguments defined in your parser as well as `content` argument holding all texts in the block.

You can find an example in [shell.py](wander/plugins/shell.py).