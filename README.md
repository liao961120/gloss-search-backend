# gloss-search-backend

## 專案目的

這個專案主要是方便於處理語言田野調查課程所採集的檔案。這學期我們請了霧台魯凱語的族語老師，並將每個禮拜採集的語料整理成一個 `.docx` 檔。

此專案承接 [`puerdon/corpus_processor`](https://github.com/puerdon/corpus_processor)，將原本的實作從 Jupyter Notebook 擴充成 Web App。


## 使用

下方有兩種使用方式：[Python 3](#python-3) 或是 [Docker](#docker)。Python 3 在每次使用時會比較麻煩；Docker 在使用上方便許多，但某些電腦可能會因軟硬體不支援而無法安裝。

### Python 3

1. (第一次使用時) 安裝 [Python 3](https://www.python.org/downloads/) (3.7 以上)

1. (第一次使用時) [下載](https://github.com/liao961120/corpus_processor/archive/master.zip)並解壓 `corpus_processor-master.zip`

1. (第一次使用時) 開啟 Terminal (e.g. `命令提示字元`)，更換工作目錄至 `corpus_processor-master/`，並執行

    ```bash
    # cd /path/to/corpus_processor-master/
    pip install -r requirements.txt
    ```

1. 將語料放置於此資料夾內的 `corp/`
    
    ```
    corpus_processor-master/    # uncompressed root folder
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

1. 開啟 Terminal，更換工作目錄至 `corpus_processor-master/`

    ```bash
    cd /path/to/corpus_processor-master/
    ```

1. 執行程式

    ```bash
    python server.py  # or python3 server.py
    ```

1. 前往 <https://glosss.yongfu.name> 查詢語料

    - 勾選 `Gloss`: 搜尋 interlinear gloss (e.g. 族語, `主格`, `OBJ` 等)
        - 支援 RegEx 搜尋
    - 勾選 `Notes`: 搜尋 `#e`, `#c`, 與 `#n` 的內容
    - 若要尋找**同時含有**多項內容時，使用 `,` 分隔搜尋內容。例如，想搜尋同時包含 `主格`, `ki` 以及 `Takanaw` 的語料，可輸入：
        
        ```
        主格,ki,Takanaw
        ```

    ![[Demo](https://img.yongfu.name/gif/gloss-search.gif)](https://img.yongfu.name/gif/gloss-search.gif)


### Docker

1. (第一次使用時) 安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)  
    **請注意電腦硬體及作業系統需求**

1. (第一次使用時) 開啟 Terminal (e.g. `Powershell`, `命令提示字元`) 下載 docker image

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
    - 若要尋找**同時含有**多項內容時，使用 `,` 分隔搜尋內容。例如，想搜尋同時包含 `主格`, `ki` 以及 `Takanaw` 的語料，可輸入：
        
        ```
        主格,ki,Takanaw
        ```
    
    ![[Demo](https://img.yongfu.name/gif/gloss-search.gif)](https://img.yongfu.name/gif/gloss-search.gif)


## 語料檔範例

```
1.
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

## 語料檔格式
```
[編號].
[族語轉寫]
[英文Glossing]
[中文Glossing]
[空行]
#e [英文翻譯]
#c [中文翻譯]
#n [註釋]
[空行]
```
