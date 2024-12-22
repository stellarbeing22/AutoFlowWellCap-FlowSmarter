import subprocess

python_executable = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\python.exe"  # Full path to the Python executable in your virtual environment
script_path = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\Uttrakhandmap.py"  # Full path to the script you want to run
subprocess.run(
    [python_executable, script_path])  # Run the script using the correct Python interpreter
script_path_2 = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\uttrakhandartesians.py"  # Path to the second script you want to run
subprocess.run([python_executable, script_path_2])
