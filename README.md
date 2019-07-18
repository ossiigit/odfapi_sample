# ODF API Server 安裝

要跑範例必須要先完成 ODF API Server 的建置詳情請參考[ODF文件API工具](https://www.ndc.gov.tw/cp.aspx?n=260AB6C70F5AF292&s=04C4AB150E9149D6)


# ODF API 範例網頁環境

### 如何部屬?
```
pip install -r requirements.txt

或是

conda install --yes --file requirements.txt

```

### 如何執行?
```
python server.py --host=0.0.0.0 --port=8080
```

### 如何修改 ODF API 網址?

ODF API 的網址修改只需要到 `conf/odfapi.py`, 修改後面的網址(這邊採用的網址都是 JSON API)

```
{
    '履歷表生成範例':'http://192.168.3.186:9980/lool/merge-to/10db8056-a485-11e9-8e17-080027f6714d',
    '報價單生成範例':'http://192.168.3.186:9980/lool/merge-to/1c934f06-a48c-11e9-8e17-080027f6714d',
}
```
