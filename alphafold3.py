'''
This script is made to run AlphaFold 3 predictions given the inputs of protein name, # of subunits, and sequence.
It generates a json file based on the inputs, then runs AlphaFold 3 on the given inputs
'''

import json
import os
import subprocess

name = input("Enter the name of the protein: ")
while True:
  try:
    n = int(input("Enter the number of polypeptide subunits in the oligomer"))
    if (n >= 1 and n <= 26):
      break
    else:
      print("Invalid input, please enter an integer between 1-26")
  except ValueError:
    print("Invalid input. Please enter an integer between 1-26")

sequence = input("Enter the amino acid sequence of the protein:")

# print(name, n, sequence
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# print([alphabet[c] for c in range(n)])

data = {
  "name" = name.upper(),
  "sequences": [
      {
        "protein": {
          "id": [alphabet[c] for c in range(n)],
          "sequence": (
              sequence
                )
          }
      }
  ],
  "modelSeeds": [1],
  "dialect": "alphafold3",
  "version": 1
}

# print(data


folder_path = "/home/alphafold/af_input"
file_name = f"{name.lower()}.json"
full_path = os.path.join(folder_path, file_name)

with open(full_path, "w") as f:
  json.dump(data, f, indent = 2)

print(f"JSON saved to {full_path}")

home = os.path.expanduser("~")
working_dir = f"{home}/alphafold3"

docker_command = [
  "docker", "run", "-it",
  "--volume", f"{home}/af_input:root/af_input",
  "--volume", f"{home}/af_output:root/af_output",
  "--volume", f"{home}/af3_parameters:root/model",
  "--volume", f"{home}/af3_data:root/public_databases",
  "--gpus", "all",
  "-e", "TF_FORCE_UNIFIED_MEMORY=1",
  "-e", "XLA_CLIENT_MEM_FRACTION=3.2",
  "alphafold3",
  "python", "run_alphafold.py",
  f"--json_path=/root/af_input/{file_name}",
  "--model_dir=/root/models",
  "--output_dir=/root/af_output"
]

subprocess.run(docker_command, cwd=working_dir)
