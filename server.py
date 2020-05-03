import os
import sys
import json
import falcon
import logging
from falcon_cors import CORS
from GlossProcessor import GlossProcessor
from GlossProcessor import get_files_timestamp

logging.basicConfig(format='\n[GLOSS-SEARCH]:  %(message)s\n', datefmt='%Y/%m/%d %I:%M:%S', level=logging.INFO)

# Initialize corpus
if len(sys.argv) > 1:
    DOCX_PATH = sys.argv[1].strip()
if not os.path.exists(DOCX_PATH):
    DOCX_PATH = './corp'

FILE_TIMESTAMPS = get_files_timestamp(DOCX_PATH)
C = GlossProcessor(docs_folder_path=DOCX_PATH)


class Query(object):
    def on_get(self, req, resp):
        global FILE_TIMESTAMPS
        global DOCX_PATH
        global C

        # Reload corpus if file changed
        file_timestamps = get_files_timestamp(DOCX_PATH)
        for fn, time in file_timestamps.items():
            if fn not in FILE_TIMESTAMPS or time != FILE_TIMESTAMPS[fn]:
                logging.warning(f"File change detected (`{os.path.basename(fn)}`), reload corpus!")
                C = GlossProcessor(docs_folder_path=DOCX_PATH)   # Reload corpus
                FILE_TIMESTAMPS = file_timestamps                # Update timestamps
                break

        params = {
            'query': 'ku,ki',
            'regex': 0,
            'type': 'gloss',  # 'free'
        }
        # Parse query string
        for k, v in req.params.items():
            params[k] = v
        params['regex'] = int(params['regex'])

        ############ DEBUGGING ##############
        logging.debug("Recieved request!!!")
        ############ _DEBUGGING ##############
        
        # Search corpus
        if params['type'] == 'gloss':
            results = C.search_gloss(tokens=params['query'], regex=params['regex'])
        else:
            results = C.search_free(tokens=params['query'], regex=params['regex'])
        
        ############ DEBUGGING ##############
        logging.debug("Sending response...")
        ############ _DEBUGGING ##############

        # Response to frontend
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(results, ensure_ascii=False)
        
        ############ DEBUGGING ##############
        logging.debug("Response sent !!!")
        ############ _DEBUGGING ##############
   

#---------- API settings -----------#
# falcon.API instances are callable WSGI apps
cors = CORS(allow_all_origins=True)  # Allow access from frontend
app = falcon.API(middleware=[cors.middleware])

# Resources are represented by long-lived class instances
searchGloss = Query()

# things will handle all requests to the '/things' URL path
app.add_route('/query', searchGloss)



if __name__ == '__main__':
    from wsgiref import simple_server

    port = 1420
    print(f"Start serving at http://localhost:{port}")
    httpd = simple_server.make_server('localhost', port, app)
    httpd.serve_forever()