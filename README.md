# gloss-search

**中文** | [English](./README-en.md)

## 專案目的

這個專案主要是方便於處理[語言田野調查課程](https://nol2.aca.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=142%20M0210&class=&dpt_code=1420&ser_no=10017&semester=108-2&lang=CH)所採集的檔案。這學期我們請了霧台魯凱語的族語老師，並將每個禮拜採集的語料整理成一個 `.docx` 檔。

此專案承接 [`puerdon/corpus_processor`](https://github.com/puerdon/corpus_processor)，將原本的實作從 Jupyter Notebook 擴充成 Web App。


## 使用

### Dependencies: Python 3

若電腦沒有 [Python 3](https://www.python.org/downloads/) (3.7 以上)，請先安裝 (可見此[安裝教學](https://lopentu.github.io/PythonForHumanities/slides/week2.html#/))。接著請[下載](https://github.com/liao961120/gloss-search/archive/master.zip)並解壓 `gloss-search-master.zip`。

### `run_app.py`

直接執行 `gloss-search-master/` 裡的 `run_app.py` 是最簡單的使用方式。在 (第一次) 執行前，請先修改 `run_app.py` 內的**檔案路徑** (至 `server.py` 以及 Word 文件所在之資料夾)。(以 Windows 為例，) 若你將 `gloss-search-master/` 置於**桌面**，且桌面有另一**存放語料檔 (`.docx`) 的資料夾** (`Linguistic_Fieldwork/`)，則要至 `run_app.py` 將其中的這兩行改成這樣 （請修改下方的`<使用者名稱>`）：

```python
SERVER_SCRIPT_PATH = r'C:\Users\<使用者名稱>\Desktop\gloss-search-master\server.py'  # 主程式路徑
DOCX_FOLDER_PATH = r'C:\Users\<使用者名稱>\Desktop\Linguistic_Fieldwork'             # 語料檔資料夾
```

完成此設置後，只要**不更動語料檔資料夾及主程式資料夾位置**，下次在執行此程式時，僅需下方的兩個步驟即可：

1. 開啟 Terminal 執行 `run_app.py` (注意作業系統)

    ```bash
    python run_app.py    # if you're on Windows
    python3 run_app.py   # if you're on Mac
    ```

1. 前往 <https://glosss.yongfu.name> 查詢語料

    - 勾選 `Gloss`: 搜尋 interlinear gloss (e.g. 族語, `主格`, `OBJ` 等)
        - 支援 RegEx 搜尋
    - 勾選 `Notes`: 搜尋 `#e`, `#c`, 與 `#n` 的內容
    - 若要尋找**同時含有**多項內容時，使用 `,` 分隔搜尋內容。例如，想搜尋同時包含 `主格`, `ki` 以及 `Takanaw` 的語料，可輸入 `主格,ki,Takanaw`
    
    ![Demo](https://img.yongfu.name/gif/gloss-search-min.gif)

---

## 語料檔

#### 範例

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

#### 格式
```
[編號].
[族語轉寫(原始, Optional)]
[族語分析(aligned)]
[英文Glossing]
[中文Glossing]
[空行]
#e [英文翻譯]
#c [中文翻譯]
#n [註釋]
[空行]
```

---

## Developer's Notes

### Python Usage

1. (第一次使用時) 開啟 Terminal，更換工作目錄至 `gloss-search-master/`，並執行

    ```bash
    # cd /path/to/corpus_processor-master/
    pip install -r requirements.txt
    ```

1. 將語料放置於此資料夾內的 `corp/`
    
    ```
    gloss-search-master/        # uncompressed root folder
    │
    ├── corp/                   # put glossing docx here
    │   ├── 20200318.docx
    │   ├── 20200325.docx
    │   └── 20200408-test.docx
    │
    ├── corpus_processor.ipynb
    ├── Dockerfile
    ├── GlossProcessor.py
    ├── README.md
    ├── requirements.txt
    └── server.py
    ```

1. 開啟 Terminal，更換工作目錄至 `gloss-search-master/`

    ```bash
    cd /path/to/gloss-search-master/
    ```

1. 執行程式

    ```bash
    python server.py    # on Windows
    python3 server.py   # on Mac
    ```

1. 前往 <https://glosss.yongfu.name> 查詢語料

    - 勾選 `Gloss`: 搜尋 interlinear gloss (e.g. 族語, `主格`, `OBJ` 等)
        - 支援 RegEx 搜尋
    - 勾選 `Notes`: 搜尋 `#e`, `#c`, 與 `#n` 的內容
    - 若要尋找**同時含有**多項內容時，使用 `,` 分隔搜尋內容。例如，想搜尋同時包含 `主格`, `ki` 以及 `Takanaw` 的語料，可輸入 `主格,ki,Takanaw`



### Docker Usage


1. (第一次使用時) 開啟 Terminal 下載 docker image

    ```bash
    docker pull liao961120/gloss-search
    ```

1. 更換工作目錄至 `*.docx` 檔案所在之資料夾

    ```bash
    # Change working dir to the folder where you put your glossing files (.docx)
    cd path/to/glossing/glossing/folder
    ```

1. 執行 docker image `liao961120/gloss-search` (注意作業系統)

    ```bash
    # Unix-like bash: cd to `corp/` and run:
    docker container run -it -p 127.0.0.1:1420:80 -v $(pwd):/usr/src/app/corp/ liao961120/gloss-search

    # Windows cmd: cd to `corp/` and run
    docker container run -it -p 127.0.0.1:1420:80 -v %cd%:/usr/src/app/corp/ liao961120/gloss-search

    # Windows PowerShell: cd to `corp/` and run
    docker container run -it -p 127.0.0.1:1420:80 -v ${PWD}:/usr/src/app/corp/ liao961120/gloss-search
    ```

1. 前往 <https://glosss.yongfu.name> 查詢語料

    - 勾選 `Gloss`: 搜尋 interlinear gloss (e.g. 族語, `主格`, `OBJ` 等)
        - 支援 RegEx 搜尋
    - 勾選 `Notes`: 搜尋 `#e`, `#c`, 與 `#n` 的內容
    - 若要尋找**同時含有**多項內容時，使用 `,` 分隔搜尋內容。例如，想搜尋同時包含 `主格`, `ki` 以及 `Takanaw` 的語料，可輸入 `主格,ki,Takanaw`
