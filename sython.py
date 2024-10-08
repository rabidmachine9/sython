import sys
from sython_interpreter import SythonInterpreter  # Import your interpreter class

def repl():
    """Basic REPL for the Sython interpreter."""
    sython = SythonInterpreter()  # Instantiate the interpreter
    print("Sython REPL - Scheme Interpreter")
    while True:
        try:
            code = input('sython> ')
            if code.lower() in ['exit', 'quit']:
                break
            result = sython.run(code)  # Use the instance's run method
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

def run_script(file_path):
    """Run a .sy script file."""
    sython = SythonInterpreter(debug=True)  # Instantiate the interpreter
    with open(file_path, 'r') as f:
        code = f.read()
    result = sython.run(code)  # Use the instance's run method
    if result is not None:
        print(result)

def main():
    if len(sys.argv) > 1:
        # If a file is provided, run the script
        script_path = sys.argv[1]
        if script_path.endswith(".sy"):
            run_script(script_path)
        else:
            print(f"Error: {script_path} is not a .sy file")
    else:
        # No arguments provided, launch REPL
        repl()

if __name__ == "__main__":
    main()