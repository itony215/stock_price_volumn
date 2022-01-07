# stock_price_volumn
定時抓取股價及量
## Usage

```
python get_price_volumn.py
```

## Cron Job
每天晚上9點30抓取
#### 編輯crontab -e
```
30 21 * * * /usr/bin/python3 /home/pitaya/Documents/stock/get_price_volumn.py >> /home/pitaya/Documents/stock/result.txt 2>&1
```
