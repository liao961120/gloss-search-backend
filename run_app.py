'''
Python script for running the app (cross platform)

Usage: 
  On Mac:      python3 run_app.py
  On Windows:  python run_app.py

  Please set the correct ABSOLUTE PATHs to server.py and the corpus folder 
  in SERVER_SCRIPT_PATH & DOCX_FOLDER_PATH
'''

# For the first time (or when you change where you put things), 
# please set the paths to server.py and 
# the corpus data (the folder where you put docx files in)
# On windows, should be something like:
#SERVER_SCRIPT_PATH = r'C:\Users\liao\Desktop\gloss-search-backend\server.py'
#DOCX_FOLDER_PATH = r'C:\Users\liao\Desktop\Linguistic_Fieldwork'
# On Mac, should be something like:
#SERVER_SCRIPT_PATH = r'/Users/liao/corpus_processor/server.py'
#DOCX_FOLDER_PATH = r'/Users/liao/Desktop/Linguistic_Fieldwork'
# On Linux, should be something like:
SERVER_SCRIPT_PATH = r'/home/liao/corpus_processor/server.py'
DOCX_FOLDER_PATH = r'/home/liao/Desktop/108-2/Linguistic_Fieldwork/'



#-------- DO NOT TOUCH ANYTHING BELOW --------#
import os
import sys
import pathlib
import subprocess
import pkg_resources

# Setup os specific parameters
python = sys.executable
SERVER_SCRIPT_PATH = pathlib.Path(SERVER_SCRIPT_PATH)
DOCX_FOLDER_PATH = pathlib.Path(DOCX_FOLDER_PATH)


# Check & install dependencies
required = {'falcon', 'falcon-cors', 'python-docx'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    print(f"Installing required python modules: {', '.join(missing)} ...")
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# Check exist
if not SERVER_SCRIPT_PATH.is_file():
    raise Exception(f"Script: `{SERVER_SCRIPT_PATH}` does not exist.")
if not DOCX_FOLDER_PATH.is_dir():
    raise Exception(f"Folder: `{DOCX_FOLDER_PATH}` does not exist.")

# Get python name (python or python3)
# Start server
subprocess.run([python, str(SERVER_SCRIPT_PATH), str(DOCX_FOLDER_PATH)])
