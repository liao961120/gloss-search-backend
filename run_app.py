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
SERVER_SCRIPT_PATH = 'C:/Users/liao/Desktop/gloss-search-backend/server.py'
DOCX_FOLDER_PATH = 'C:/Users/liao/Desktop/Linguistic_Fieldwork/'
# On Mac, should be something like:
#SERVER_SCRIPT_PATH = '/Users/liao/corpus_processor/server.py'
#DOCX_FOLDER_PATH = '/Users/liao/Desktop/Linguistic_Fieldwork'



#-------- DO NOT TOUCH ANYTHING BELOW --------#
import os
import sys
import subprocess
import pkg_resources

python = sys.executable

# Check & install dependencies
required = {'falcon', 'falcon-cors', 'python-docx'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    print(f"Installing required python modules: {', '.join(missing)} ...")
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# Check exist
if not os.path.exists(SERVER_SCRIPT_PATH):
    raise Exception(f"Script: `{SERVER_SCRIPT_PATH}` does not exist.")
if not os.path.exists(DOCX_FOLDER_PATH):
    raise Exception(f"Folder: `{DOCX_FOLDER_PATH}` does not exist.")

# Get python name (python or python3)
# Start server
subprocess.run([python, SERVER_SCRIPT_PATH, DOCX_FOLDER_PATH])
