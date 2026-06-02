import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given file which is relative to the working directory. arguments are optional and are used to pass when running the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file name of the file to run. the file is relative to the working_directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An array of strings containing the content to write to the file",
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # check if file_path is inside working_directory
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))
        valid_target_dir = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        completed_process_object = subprocess.run(command,
                                cwd=wd_absolute_path,
                                capture_output=True,
                                text=True,
                                timeout=30)
        return_string_list = []
        return_stdout = completed_process_object.stdout
        return_stderr = completed_process_object.stderr
        return_code = completed_process_object.returncode
        if return_code != 0:
            return_string_list.append(f"Process exited with code {return_code}")
        if return_stdout:
            return_string_list.append(f"STDOUT: {return_stdout}")
        if return_stderr:
            return_string_list.append(f"STDERR: {return_stderr}")
        return '\n'.join(return_string_list)
    except Exception as e:
        return f"Error: executing Python file: {e}"