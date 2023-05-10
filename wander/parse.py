import re
import subprocess
from utils import read_file, write_file
import argparse

def parse_custom_arguments(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--output-error", action="store_true", help="Enable verbose mode")
    # parser.add_argument("--name", help="Specify a name")

    # Split the provided arguments into a list
    args_list = arguments.split()

    # Parse the arguments
    args = parser.parse_args(args_list)
    return args

def replace_shell_command(command, output_error: bool):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()
        return output
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode().strip()
        if output_error:
            return f"Error executing command:\n{command}\n\n{error_output}"
        else:
            raise subprocess.CalledProcessError(error_output)


def parse_shell_directive(match):
    if match[2] == "":
        arguments = ""
        command = match[1].strip()
    
    else:
        arguments = match[1].strip()
        command = match[2].strip()

    if command == "":
        raise ValueError("Must specify a command in the block")
    
    arguments = parse_custom_arguments(arguments)
    arguments = namespace_to_dict(arguments)
    return replace_shell_command(command, **arguments)

def namespace_to_dict(namespace):
    return {
        k: namespace_to_dict(v) if isinstance(v, argparse.Namespace) else v
        for k, v in vars(namespace).items()
    }

def parse(markdown_text):
    pattern = r'```!shell\s+([^\n]+)\n(.*?)```'
    replaced_text = re.sub(pattern, parse_shell_directive, markdown_text, flags=re.DOTALL)
    return replaced_text

if __name__ == "__main__":
    markdown_file_path = './data/example.md'
    replaced_text = parse(read_file(markdown_file_path))
    print(replaced_text)
