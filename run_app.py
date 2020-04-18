####################################################
# Usage: python startup_script_cross_platform.py
# Python script for starting the server,
# without need to setting up working dir 
# and corpus path.
#
# Please setup the correct paths for the first time.
####################################################

# Please use absolute path, e.g. /Users/username/Desktop/gloss-search-backend
SERVER_SCRIPT_PATH = 'C:/Users/username/Desktop/gloss-search-backend/server.py'
DOCX_FOLDER_PATH = 'C:/Users/username/Desktop/Linguistic_Fieldwork/'
#SERVER_SCRIPT_PATH = '/home/liao/corpus_processor/server.py'
#DOCX_FOLDER_PATH = '/home/liao/corpus_processor/corp'

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
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# Check exist
if not os.path.exists(SERVER_SCRIPT_PATH):
    raise Exception(f"Script: `{SERVER_SCRIPT_PATH}` does not exist.")
if not os.path.exists(DOCX_FOLDER_PATH):
    raise Exception(f"Folder: `{DOCX_FOLDER_PATH}` does not exist.")

# Get python name (python or python3)
# Start server
subprocess.run([python, SERVER_SCRIPT_PATH, DOCX_FOLDER_PATH])
