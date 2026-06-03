# AI Coding Agent (Python)

A small command-line AI coding assistant built with Python and the Gemini API.

This project explores how modern AI agents work using tool/function calling. The agent can inspect files, read file contents, execute Python scripts, and write files inside a restricted working directory.

The goal of this project was to better understand:

* AI agent loops
* function/tool calling
* filesystem interaction
* subprocess execution
* path sandboxing/security
* modular Python project structure

---

## Features

* Read files from a project directory
* List files and directories
* Execute Python scripts with optional arguments
* Write or overwrite files
* Tool/function calling using the Gemini API
* Basic sandboxing to prevent access outside the working directory
* Verbose mode for debugging token usage and tool calls

---

## Example

```bash
uv run main.py "List all files in the pkg directory"
```

Example output:

```text
Response:
 - Calling function: get_files_info
Response:
Here are the files in the `pkg` directory:

*   `__pycache__` (directory)
*   `render.py`
*   `morelorem.txt`
*   `calculator.py`
```

---

# How It Works

The program runs in a loop where:

1. The user sends a prompt
2. Gemini decides whether tools/functions are needed
3. Python executes the requested tool
4. The result is returned back to the model
5. The model continues until it produces a final response

The agent currently supports:

* file inspection
* file reading
* writing files
* executing Python scripts

---

# Security Notes

The project includes basic path validation to prevent files outside the allowed working directory from being accessed.

For example:

* `../../etc/passwd` would be rejected
* only files inside the configured working directory are allowed

This was implemented using normalized absolute paths and `os.path.commonpath`.

---

# Technologies Used

* Python
* Gemini API
* python-dotenv
* argparse
* subprocess
* modular function/tool architecture

---

# Running The Project

## 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-name>
```

## 2. Create a virtual environment

```bash
uv venv
```

Activate it:

### Linux / WSL

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
uv sync
```

or manually:

```bash
uv add google-genai python-dotenv
```

## 4. Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

## 5. Run the agent

```bash
uv run main.py "Read the contents of main.py"
```

Verbose mode:

```bash
uv run main.py "List files" --verbose
```

---

# Things I Learned

* How AI function/tool calling works
* How conversational agent loops operate
* Why path validation matters
* How subprocess execution works in Python
* Structuring Python projects into smaller modules
* Managing model responses and tool outputs


