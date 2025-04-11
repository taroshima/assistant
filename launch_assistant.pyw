import subprocess
import os

script_path = os.path.abspath("my_assistant.py")

subprocess.Popen(
    ["python", script_path],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)