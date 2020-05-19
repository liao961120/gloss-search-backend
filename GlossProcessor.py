import os
import re
import sys
import json
import pathlib
import logging
from datetime import datetime
from docx import Document

PERSON_NAMES = {'Takanaw', 'Elrenge', 'Kui', 'Lavakaw', 'Lavurase', 'Tingangurucu ', 'Lavausu', 'Muni', 'Balenge', 'Laucu', 'Tanebake', 'Kaku'}


class GlossProcessor:

    def __init__(self, docs_folder_path='.'):
        """[summary]
        
        Parameters
        ----------
        docs_folder_path : str, optional
            Path to docx files, defaults to the current dir.
        
        Notes
        ----------
        self.data structure:
        
        {
        '20200325.docx': [
            (1, {
                'ori': ['yakay', 'ku', 'tatulru', 'ku', 'ababay/sauvalay', 'ku', 'agili'],
                'gloss': [
                    ('yakay', 'have', '有'),
                    ('ku', 'three', '3'),
                    ('tatulru', 'female/male', '女性/男性'),
                    ('(ku', 'yonger_brother/sister-1SG.POSS', '弟妹-我的.第一人稱單數.所有格'),
                    ('ababay/sauvalay)', '_', '_'),
                    ('ku', '_', '_'),
                    ('agi-li', '_', '_')
                    ],
                'free': [
                    '#e I have 3 younger brother/sister',
                    '#c 我有 3 個弟弟/妹妹',
                    '#n  yakay ku 可省略'
                    ]
                }
            ),
            (2, ...),
        
        ...

        '20200408.docx': [...],
        }
        """

        self.data = {}
        self._load_data(docs_folder_path)


    def _load_data(self, path):
        path = pathlib.Path(path)
        
        for fp in path.rglob('*.docx'):
            try:
                glosses = process_doc(str(fp))
            except:
                logging.warning(f"{fp} #__:  invalid DOCX  formatting")
                continue
            self.data[str(fp)] = tokenize_glosses(glosses, str(fp))


    def search_gloss(self, tokens: str, regex=False):
        
        # Parse into a list of tokens
        if ',' in tokens:
            tokens = [ tk.strip() for tk in tokens.split(',') ]
        else:
            tokens = [ tokens.strip() ]

        # Search through all word documents
        matched_glosses = []
        for doc_id, doc in self.data.items():
            for gloss_id, gloss in enumerate(doc):
                
                # Get tokens from aligned lines
                gloss_tokens = { tk for tup in gloss[1]['gloss'].copy() for tk in tup }
                # Get tokens from original language line
                for tk in gloss[1]['ori']:
                    gloss_tokens.add(tk)

                # Check all tokens presented in gloss
                matched_num = 0
                for tk in tokens:
                    if regex:
                        if sum( 1 for g_tk in gloss_tokens if re.search(tk, g_tk) ) > 0:
                            matched_num += 1
                    else:
                        if tk in gloss_tokens:
                            matched_num += 1
                if matched_num == len(tokens):
                    matched_glosses.append({
                        'file': doc_id,
                        'num': gloss[0],
                        'ori': gloss[1]['ori'],
                        'gloss': gloss[1]['gloss'],
                        'free': gloss[1]['free'],
                    })
        
        # Return results
        return matched_glosses



    def search_free(self, tokens: str, regex=False):

        # Parse into a list of tokens
        if ',' in tokens:
            tokens = [ tk.strip() for tk in tokens.split(',') ]
        else:
            tokens = [ tokens.strip() ]

        # Search through all word documents
        matched_glosses = []
        for doc_id, doc in self.data.items():
            for gloss_id, gloss in enumerate(doc):
                
                free_content = '\n'.join(l[2:].strip() for l in gloss[1]['free'])

                # Check all tokens presented in gloss
                matched_num = 0
                for tk in tokens:
                    if regex:
                        if re.search(tk, free_content):
                            matched_num += 1
                    else:
                        if tk in free_content:
                            matched_num += 1
                if matched_num == len(tokens):
                    matched_glosses.append({
                        'file': doc_id,
                        'num': gloss[0],
                        'ori': gloss[1]['ori'],
                        'gloss': gloss[1]['gloss'],
                        'free': gloss[1]['free'],
                    })
        
        # Return results
        return matched_glosses
        


#--------------- Helper functions -------------------#
def process_doc(fp="corp/20200325.docx"):

    # Normalize document into a list of lines
    d = Document(fp)
    a_doc = '\n'.join(p.text for p in d.paragraphs)
    a_doc = a_doc.split('\n')

    # Find the positions of each elicitation
    pat_start = re.compile("^(\d{1,2})\.\s*$")
    glosses_on = []
    gloss_num_old = None
    for i, line in enumerate(a_doc):
        if pat_start.match(line):
            gloss_num_new = i

            # Save each elicitation range
            if gloss_num_old is not None:
                glosses_on.append( (gloss_num_old, gloss_num_new - 1) )
            gloss_num_old = gloss_num_new
    
    # Save last gloss
    i = gloss_num_old
    while True:
        i += 1
        if a_doc[i].strip().startswith('#'):
            if len(a_doc) == i + 1 or (not a_doc[i + 1].strip().startswith('#')):
                end_idx = i + 1
                break
    glosses_on.append( (gloss_num_old, i) )

    # Get all elicitations in the document
    glosses = []
    for start, end in glosses_on:
        gloss_num = int(re.match("(\d+)\.", a_doc[start])[1])
        gloss_lines = [ l.strip() for l in a_doc[(start + 1):end] ]
        glosses.append( (gloss_num, gloss_lines) )
    
    return glosses



def assign_gloss_free_lines(gloss):
    
    free_lines = []
    gloss_lines = []
    
    for lid, l in enumerate(gloss.copy()):
        # Skip empty lines
        if l == '': continue

        # Assign Gloss/Free lines
        if l.startswith('#'):
            free_lines.append(l)
        else:
            gloss_lines.append(l)

    return gloss_lines, free_lines # ['\n'.join(l) for l in free_lines]



def tokenize_glosses(glosses, filname):

    parsed_glosses = []
    for gloss_id in range(len(glosses)):

        gloss_lines, free_lines = assign_gloss_free_lines(glosses[gloss_id][1])

        #print(glosses[gloss_id][1])
        # 3*n + n
        num_of_lines = len(gloss_lines) 

        if num_of_lines % 3 != 0 and (num_of_lines - 1) % 3 !=0:
            logging.warning(f"{filname} #{glosses[gloss_id][0]:<2}:  invalid GLOSS formatting")
            continue
        
        # Deal with two possible formats: gloss with/without original language
        if (num_of_lines - 1) % 3 == 0:
            ori_lang = gloss_lines.pop(0)
            num_of_lines -= 1
        else:
            ori_lang = ''

        # Concat multiple lines to three
        rk_gloss = ''
        en_gloss = ''
        zh_gloss = ''
        for i in range(int(num_of_lines / 3)):
            rk_gloss += gloss_lines[0 + i * 3] + '\t'
            en_gloss += gloss_lines[1 + i * 3] + '\t'
            zh_gloss += gloss_lines[2 + i * 3] + '\t'

        # Convert gloss lines to lists
        ori_lang = ori_lang.strip().split()
        rk_gloss = rk_gloss.strip().split()
        en_gloss = en_gloss.strip().split()
        zh_gloss = zh_gloss.strip().split()

        # Check gloss alignment
        if len(rk_gloss) != len(en_gloss):
            logging.warning(f"{filname} #{glosses[gloss_id][0]:<2}: ALIGNMENT > English gloss line has {'MORE' if len(rk_gloss) < len(en_gloss) else 'LESS'} tokens than Original langauge")
        if len(rk_gloss) != len(zh_gloss):
            logging.warning(f"{filname} #{glosses[gloss_id][0]:<2}: ALIGNMENT > Chinese gloss line has {'MORE' if len(rk_gloss) < len(zh_gloss) else 'LESS'} tokens than Original langauge")
        
        # Tokenize
        gloss = []
        en_len = len(en_gloss)
        zh_len = len(zh_gloss)
        for i, rk in enumerate(rk_gloss):

            if not i < en_len:
                en = '_'
            else:
                en = en_gloss[i]
            
            if not i < zh_len:
                zh = '_'
            else:
                zh = zh_gloss[i]

            # Normalize Capital letter
            if i == 0 and rk[0].isupper():
                global PERSON_NAMES
                if rk not in PERSON_NAMES:
                    rk = rk[0].lower() + rk[1:]

            gloss.append( (rk, en, zh) )

        # Save data
        parsed_glosses.append(
            
           (glosses[gloss_id][0], 
            {
            'ori': ori_lang,
            'gloss': gloss,
            'free': [l for l in free_lines if l != '']
            }
           )
        )
    
    return parsed_glosses



def get_files_timestamp(dir):
    data = {}
    for filename in os.listdir(dir):
        if filename.endswith('.docx') or filename.endswith('.doc'):
            fp = os.path.join(dir, filename)
            data[fp] = os.stat(fp).st_mtime
    
    return data



if __name__ == "__main__":
    DOCX_FOLDER_PATH = r'2020_Budai_Rukai/'
    GDRIVE_URL = sys.argv[1]

    logging.basicConfig(level=logging.INFO, format='%(message)s', filemode='w', filename=f'{DOCX_FOLDER_PATH.strip("/")}.log')
    logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

    # Download from GDrive
    cmd = f'curl gdrive.sh | bash -s {GDRIVE_URL} > curl_download.log'
    os.system(cmd)

    os.chdir(DOCX_FOLDER_PATH)
    DOCX_FOLDER_PATH = pathlib.Path('.')

    # Format docx filename
    pat_fn = re.compile(r'\d{4,}')
    for fp in DOCX_FOLDER_PATH.rglob('*.docx'):
        new_fn = pat_fn.search(str(fp))
        if new_fn:
            new_fp = str(fp).replace(fp.name, f"{new_fn[0]}.docx")
            os.rename(str(fp), new_fp)


    C = GlossProcessor(docs_folder_path=DOCX_FOLDER_PATH)

    # Flatten data to match frontend json format
    output_glosses = []
    for docname, glosses in C.data.items():
        for gloss_num, gloss in glosses:
            gloss.update({
                'file': docname,
                'num': gloss_num,
            })
            output_glosses.append(gloss)
    
    # Write to json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_glosses, f, ensure_ascii=False)


    #-------- Get glossary --------#
    glossary = {}
    for gloss in output_glosses:
        id_ = f"{gloss['file']}#{gloss['num']}"

        gloss_set = { '=00000='.join(tup) for tup in gloss['gloss'] }

        for tk in [x.split('=00000=') for x in gloss_set]:
            
            # Normalize token pattern
            tk = [ t.strip('()/*?+-_,!.1234567890[]') for t in tk ]
            tk[0] = tk[0].lower()
            if tk[0] in [''] + list(PERSON_NAMES): continue
            
            sense = ' | '.join(t.strip() for t in tk[1:] if t.strip() != '')
            if sense == '': continue
            
            if tk[0] not in glossary:
                glossary[tk[0]] = {
                    sense: [id_],
                }
            else:
                if sense not in glossary[tk[0]]:
                    glossary[tk[0]][sense] = [id_]
                else:
                    glossary[tk[0]][sense].append(id_)

    # Sort and index for search
    sorted_glossary = []
    for k in sorted(glossary.keys()):
        
        tokens = set()

        # Add lexical entry
        tokens.add(k)
        tokens.add(k.replace('-', ''))

        # Add sense
        for sense in glossary[k]:
            for tk in sense.split('|'):
                tokens.add(tk.strip())

        # Save sorted gloss
        sorted_glossary.append( (k, glossary[k], list(tokens)) )


    with open('glossary.json', 'w') as f:
        json.dump(sorted_glossary, f, ensure_ascii=False)