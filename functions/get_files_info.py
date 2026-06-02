import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

"""
directory parameter is the relative path within working directory
    the LLM can specify which directory it wants to scan
working_directory paramerter will be set by us
    we can limit the scope of directories and files the LLM can view
"""
def get_files_info(working_directory: str, directory: str = ".") -> str:
    # validate path to directory is inside working_directory
    wd_absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(wd_absolute_path, directory))
    # True of False if directory in working_directory
    valid_target_dir = os.path.commonpath([wd_absolute_path, target_dir]) == wd_absolute_path
    return_string_list = []
    if directory == '.':
        return_string_list.append("Result for current directory:")
        # print("Result for current directory:")
    else:
        return_string_list.append(f"Result for '{directory}' directory:")
        # print(f"Result for '{directory}' directory:")
    if not valid_target_dir:
        return_string_list.append(f'   Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return '\n'.join(return_string_list)
    if not os.path.isdir(target_dir):
        return_string_list.append(f'   Error: "{directory}" is not a directory')
        return '\n'.join(return_string_list)
    # else:
    #     return f'Success: "{directory}" is within the working directory'
    target_dir_contents = os.listdir(target_dir)
    # print(target_dir_contents) # ['pkg', 'main.py', 'tests.py']
    try:
        for item in target_dir_contents:
            item_path = os.path.normpath(os.path.join(target_dir, item))
            item_size = os.path.getsize(item_path)
            item_isdir = os.path.isdir(item_path)
            # print(f"- {item}: file_size={item_size} bytes, is_dir={item_isdir}")
            return_string_list.append(f"   - {item}: file_size={item_size} bytes, is_dir={item_isdir}")
        return '\n'.join(return_string_list)
    except Exception as e:
        return_string_list.append(f"Error: {e}")
        return '\n'.join(return_string_list)
