#!/usr/bin/env python3
"""
Run all JSON files in ~/af_input/test_folder/ through AlphaFold3 Docker container.
Each JSON is processed one at a time (sequentially).
"""

import os
import subprocess
import time
from pathlib import Path

# Paths
HOME = os.path.expanduser("~")
AF_INPUT = f"{HOME}/af_input/test_folder"
AF_OUTPUT = f"{HOME}/af_output"
AF_PARAMS = f"{HOME}/af3_parameters"
AF_DATA = f"{HOME}/af3_data"

def get_json_files():
    """Get all .json files in af_input/test_folder directory."""
    input_dir = Path(AF_INPUT)
    if not input_dir.exists():
        print(f"Error: Directory {AF_INPUT} does not exist")
        return []
    json_files = sorted([f for f in input_dir.glob("*.json") if f.is_file()])
    return json_files

def run_alphafold(json_path):
    """Run AlphaFold3 Docker command for a single JSON file."""
    json_name = json_path.name
    print(f"Running: {json_name}")
    
    docker_cmd = [
        "docker", "run", "-it",
        "--volume", f"{HOME}/af_input:/root/af_input",
        "--volume", f"{HOME}/af_output:/root/af_output",
        "--volume", f"{HOME}/af3_parameters:/root/models",
        "--volume", f"{HOME}/af3_data:/root/public_databases",
        "--gpus", "all",
        "-e", "TF_FORCE_UNIFIED_MEMORY=1",
        "-e", "XLA_CLIENT_MEM_FRACTION=3.2",
        "alphafold3",
        "python", "run_alphafold.py",
        f"--json_path=/root/af_input/test_folder/{json_name}",
        "--model_dir=/root/models",
        "--output_dir=/root/af_output"
    ]
    
    start = time.time()
    result = subprocess.run(docker_cmd, cwd=HOME)
    elapsed = time.time() - start
    
    if result.returncode == 0:
        print(f"Completed: {json_name} ({elapsed/60:.1f} min)")
    else:
        print(f"Failed: {json_name} (exit code: {result.returncode})")
    
    return result.returncode

def main():
    json_files = get_json_files()
    
    if not json_files:
        print("No JSON files found in ~/af_input/test_folder/")
        return
    
    print(f"Found {len(json_files)} JSON file(s):")
    for f in json_files:
        print(f"  - {f.name}")
    
    print("\nStarting batch run...")
    print("Press Ctrl+C to cancel at any time.\n")
    
    success_count = 0
    fail_count = 0
    
    for json_file in json_files:
        rc = run_alphafold(json_file)
        if rc == 0:
            success_count += 1
        else:
            fail_count += 1
    
    print(f"Batch complete: {success_count} succeeded, {fail_count} failed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBatch cancelled by user")
