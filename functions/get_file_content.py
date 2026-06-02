import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string of maximum of 10000 chars from a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file name of the file to read from. the file is relative to the working_directory",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # validate path to directory is inside working_directory
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))
        # True of False if directory in working_directory
        valid_target_dir = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, 'r') as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"