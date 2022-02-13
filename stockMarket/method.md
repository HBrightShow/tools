1. install env:
sudo apt-get install python3.8
sudo apt-get install python3.8-pip3
pip3 install easyquotation
pip3 install easyquotation --upgrade

remark: python version must be behind on v3.6

2.detail para and use method:
    --info: if value is 'detail', it will show more information. default:'sample'.
    --color: if value is 'open', show red if rise, show blue if down. default:'close'.
    --cycle: if value is 'open', program will auto get market data , default:'close'.
    --snap: how many seconds get data from network, default:6
    --sort: sort all stock data by line, only 'now_precent' at work currently. default:'now_precent'.

    example: python3 ./stock.py --color open --info detail --cycle open --sort now_precent --snap 10


