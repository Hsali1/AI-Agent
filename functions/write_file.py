import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a string passed in 'content' to a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file name of the file to write to. the file is relative to the working_directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="a string containing the content that we will write to the file 'file_path'",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # check if file_path is inside working_directory
        # validate path to directory is inside working_directory
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))
        # True of False if directory in working_directory
        valid_target_dir = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        with open(target_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'