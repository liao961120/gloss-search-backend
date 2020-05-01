# gloss-search

**English** | [中文](./README.md)

## Usage

### Dependencies: Python 3

To run this program, [Python 3](https://www.python.org/downloads/) (above 3.7) is required. Yon need to install it if you don't have it on your computer.
Then, download [`gloss-search-master.zip`](https://github.com/liao961120/gloss-search/archive/master.zip) and extract it to a folder (you would need the path to this folder later).

### `run_app.py`

There is a python script `run_app.py` inside the extracted zip file (`gloss-search-master.zip`). To use this program, you need to execute this script in the terminal. But BEFORE THE FIRST TIME you run this script, you have to edit two lines in `run_app.py` that set the absolute paths to the folder of the docx files and `server.py`, the script essential to this program:

```python
SERVER_SCRIPT_PATH = r'/Users/<username>/Desktop/gloss-search-master/server.py'  # path to gloss-search-master/server.py 
DOCX_FOLDER_PATH = r'/Users/<username>/Desktop/Linguistic_Fieldwork/'            # path to the folder of docx files
```

Suppose you use Mac and `gloss-search-master.zip` is extracted to `gloss-search-master/` on your desktop. Also, you have your interlinear glosses (`.docx` files) saved in another folder, `Linguistic_Fieldwork/`, on your desktop. Then the paths you set in `run_app.py` should look very similar to the above example, except that you have to change `<username>` to that of yours.

After this setup, you can start the program with the steps below (as long as you keep the locations of the folders constant, you won't have to repeat the steps mentioned above the next time you start the program):

1. Open the terminal and execute `run_app.py` with one of the command below (depends on your os):

    ```bash
    python run_app.py    # if you're on Windows
    python3 run_app.py   # if you're on Mac
    ```

1. Visit <https://glosss.yongfu.name> to search the docx files:

    - select `Gloss` to target the gloss lines (lines with aligned tokens)
        - search with [regular expression](https://en.wikipedia.org/wiki/Regular_expression) with `RegEx` selected
    - select `Notes` to target the free lines (those starting with `#e`, `#c`, and `#n`)
    - Concatenate multiple patterns with `,` to get glosses that **match all of them**. For instance, to get glosses that contains both `NOM` and `ki`, search with the string `NOM,ki`.

    ![Demo](https://img.yongfu.name/gif/gloss-search-min.gif)

---

## `docx` File Format

#### Example

```
1.
matassami su tigami ni Payan babay i Laway

ma-tas=sami         su     tigami     ni     Payan    babay   i    Laway
AF-write=1PL.NOM    ACC    letter     BEN    Payan    for     NOM  Laway
主焦-寫=1PL.主格     受格    信         受益格   Payan    給      主格  Laway

#e I write the letter to Laway with Payan.  
#c 我跟Payan一起寫信給Laway。   
#n 比較 ki Payan 和 ni Payan: ki Payan的意思為「和 Payan」，ni Payan的意思為「 Payan的信」。

2.
si-pa-quwas=mu           i      yaya
CF-VBL-song=1SG.GEN      NOM    mother
參焦-動化-歌=1SG.屬格      名詞    媽媽
 
#e I sing for mom.
#c 我唱歌給媽媽聽。
#n i 可以省略。
```

#### Format

```
[Number].
[Original language]
[Empty line (optional)]
[Original language (aligned)]
[English glossing (aligned)]
[Chinese glossing (aligned)]
[Empty line]
#e [English translation]
#c [Chinese translation]
#n [Notes]
[Empty line]
```
