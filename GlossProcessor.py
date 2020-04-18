import os
import re
import logging
from docx import Document


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

        for filename in os.listdir(path):
            if filename.endswith(".docx"):
                try:
                    glosses = process_doc(os.path.join(path, filename))
                except:
                    logging.warning(f"Invalid formatting in docx: `{filename}`")
                    continue
                self.data[filename] = tokenize_glosses(glosses, filename)



    def search(self, isgloss: bool, tokens: str, regex=False):
        if isgloss:
            return self.search_gloss(tokens, regex)
        else:
            return self.search_free(tokens)



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
                
                gloss_content = gloss[1]['gloss']
                gloss_tokens = { tk for tup in gloss_content for tk in tup }

                # Check all tokens presented in gloss
                matched_num = 0
                for tk in tokens:
                    if regex:
                        if sum( 1 for g_tk in gloss_tokens if re.match(tk, g_tk) ) > 0:
                            matched_num += 1
                    else:
                        if tk in gloss_tokens:
                            matched_num += 1
                if matched_num == len(tokens):
                    matched_glosses.append({
                        'file': doc_id,
                        'num': gloss[0],
                        'gloss': gloss[1]['gloss'],
                        'free': gloss[1]['free'],
                    })
        
        # Return results
        return matched_glosses



    def search_free(self, tokens: str):

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
                    if tk in free_content:
                        matched_num += 1
                if matched_num == len(tokens):
                    matched_glosses.append({
                        'file': doc_id,
                        'num': gloss[0],
                        'gloss': gloss[1]['gloss'],
                        'free': gloss[1]['free'],
                    })
        
        # Return results
        return matched_glosses
        


#--------------- Helper functions -------------------#
def process_doc(fp="corp/20200325.docx"):
    
    # Load document
    d = Document(fp)
    a_doc = '\n'.join(p.text for p in d.paragraphs)  # normalize paragraphs to newlines
    
    # Find the places of glosses
    pat_start = re.compile("^(\d{1,2})\.")
    a_doc_split = a_doc.split('\n')
    glosses_on = []
    gloss_num_old = None
    for i, line in enumerate(a_doc_split):

        if pat_start.match(line):
            gloss_num_new = i

            # Save gloss range
            if gloss_num_old is not None:
                glosses_on.append( (gloss_num_old, gloss_num_new - 1) )
            gloss_num_old = gloss_num_new

    # Get all glosses
    glosses = []
    for s, e in glosses_on:
        gloss_num = int(re.match("(\d+)\.", a_doc_split[s])[1])
        gloss_lines = [ l.strip() for l in a_doc_split[(s+1):e] ]
        glosses.append( (gloss_num, gloss_lines) )
    
    return glosses



def assign_gloss_free_lines(gloss):
    
    free_lines = ['#e', '#c', '#n']
    gloss_lines = []
    
    for lid, l in enumerate(gloss.copy()):

        # Assign free lines
        if l.startswith('#e'):
            free_lines[0] = l
        elif l.startswith('#c'):
            free_lines[1] = l
        elif l.startswith('#n'):
            free_lines[2] = l

        # Assign gloss lines
        if not (l.startswith('#e') or l.startswith('#c') or l.startswith('#n') or l.strip() == ''):
            gloss_lines.append(l.strip())

    return gloss_lines, free_lines



def tokenize_glosses(glosses, filname):

    parsed_glosses = []
    for gloss_id in range(len(glosses)):

        gloss_lines, free_lines = assign_gloss_free_lines(glosses[gloss_id][1])

        #print(glosses[gloss_id][1])
        # 3*n + n
        num_of_lines = len(gloss_lines) 

        if num_of_lines % 3 != 0:
            logging.warning(f"Invalid gloss formatting: #{glosses[gloss_id][0]} in {filname}")
            continue

        # Concat multiple lines to three
        rk_gloss = ''
        en_gloss = ''
        zh_gloss = ''
        for i in range(int(num_of_lines / 3)):
            rk_gloss += gloss_lines[0 + i * 3] + '\t'
            en_gloss += gloss_lines[1 + i * 3] + '\t'
            zh_gloss += gloss_lines[2 + i * 3] + '\t'

        rk_gloss = rk_gloss.strip().split()
        en_gloss = en_gloss.strip().split()
        zh_gloss = zh_gloss.strip().split()
        
        
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

            gloss.append( (rk, en, zh) )
        

        # Save data
        parsed_glosses.append(
            
           (glosses[gloss_id][0], 
            {
            #'ori': glosses[gloss_id][1],
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