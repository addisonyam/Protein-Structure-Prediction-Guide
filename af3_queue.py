import pandas as pd
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def read_csv():
  filepath = input("Please enter a filepath: ")

  # Read the CSV file into a DataFrame
  df = pd.read_csv(f'{filepath[1:-1]}')

  jobs = df[df['Run Status'] == 'N']
  jobs = jobs[['Run Status', 'Name', 'Sequence', 'Subunits']]
  print("The following jobs will be queued:")
  print(jobs[['Name', 'Sequence', 'Subunits']])
  resp = input("Would you like to queue the above jobs to AlphaFold 3? (Y/N)")
  while (resp != 'Y' and resp != 'N'):
    resp = input('Would you like to queue the above jobs to AlphaFold 3? (Y/N)')
  if (resp == 'N'):
    jobs = jobs.iloc[0:0]
  return jobs

def create_folder():
  from datatime import datatime

  now = datatime.now()

  timestamp_str = now.strftime("%Y-%m-%d_%H:%M")
  folder_name = f"af3job_{timestamp_str}"
  # print(folder_name)

  # Create folder path 
  folder_path = Path(f"/home/alphafold/af_input/{folder_name}")

  # Make directory
  folder_path.mkdir(parents=True, exist_ok=True)

  print(f"Folder created at {folder_path}")

  return folder_name
