# scripts_pku

### 安裝 requirements.txt 套件
```python
pip install –r requirements.txt
```

### 修改 info.py 程式碼
```python
TOTAL_PAGES = 172
# personal information below
ID = "STUDENT_ID"  # enter your ID here
NAME = "NAME_HERE"  # enter your name here
NUMBER = 0  # enter your number here
```

### 執行程式碼
#### 步驟一：生成 138 張 svg 稿紙
```python
python 1_SVGtable.py
```
#### 步驟二：將 138 張 svg 轉成 138 個 pdf 檔案
```python
python 2_SVG2PDF.py
```
#### 步驟三：將 138 張 pdf 檔案合併成一個 pdf 檔案
```python
python 33_PDFmerge.py
```
