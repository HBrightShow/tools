
import easyquotation  as eq
import time, os, threading, sys

def get_care_real_data():
    quot = eq.use('sina')   # ['sina', 'tencent', 'qq'] 
    real_data = quot.real(['000796','300205','300732'])
    stockReal = {}
    key_care = ["name", "open", "close", "now", "high", "low", "time"]
    for code in real_data:
        stockReal[code] = {}
        for key in real_data[code]:
            if key in key_care:
                stockReal[code][key] = str(real_data[code][key])
    return stockReal

def get_percent(close, now):
    first = float(close)
    second = float(now)
    if second >= first:
        precent = round((second - first) / first * 100, 2)
    else:
        precent = round((first - second) / first * 100, 2)
        precent = precent - precent * 2
    return precent

    
def deal_stock_data(stockReal):
    stock_result = {}
    #py = Pinyin()
    for code in stockReal:
        stock_result[code] = {}
        open = close = now = high = low = 0

        for key in stockReal[code]:
            if key == "name":
                #stock_result[code]["name"] = py.get_pinyin(stockReal[code][key])
                stock_result[code]["name"] = stockReal[code][key]
                #pass
            elif key == "open":
                open = stockReal[code][key]
                stock_result[code]["open"] = stockReal[code][key]
            elif key == "close":
                stock_result[code]["close"] = stockReal[code][key]
                close = stockReal[code][key]
            elif key == "now":
                now = stockReal[code][key]
                stock_result[code]["now"] = stockReal[code][key]
            elif key == "high":
                high = stockReal[code][key]
                stock_result[code]["high"] = stockReal[code][key]
            elif key == "low":
                low = stockReal[code][key]
                stock_result[code]["low"] = stockReal[code][key]
            elif key == "time":
                #stock_result[code]["time"] = stockReal[code][key]
                pass
            else:
                print("stockReal key parse failed.")
        
        open_precent = get_percent(close, open)
        stock_result[code]["open_precent"] = open_precent
        now_precent = get_percent(close, now)
        stock_result[code]["now_precent"] = now_precent
        low_precent = get_percent(close, low)
        stock_result[code]["low_precent"] = low_precent
        high_precent = get_percent(close, high)
        stock_result[code]["high_precent"] = high_precent
        swing_precent = get_percent(low, high)
        stock_result[code]["swing_precent"] = swing_precent
    return stock_result

def chinese_count(fields):
    counts = 0
    for _char in fields:
        if '\u4e00' <= _char <= '\u9fa5':
            counts += 1
    return counts

def print_to_console(title, color):
    result = ''
    tar_length = 10
    for val in title:
        # a chinese char have the length of two chars 
        cn_no = chinese_count(val)
        if cn_no > tar_length:
            cn_no = tar_length
        result += val.center(tar_length - cn_no, ' ')
    
    if color == 0:
        result = '\033[34m' + result + '\033[1m'
    elif color == 1:
        result = '\033[31m' + result + '\033[1m'
    elif color == 2:
        result = '\033[0;32;40m' + result + '\033[1m'
    else:
        result = '\033[38m' + result + '\033[1m'
        #pass
    print(result)  

def print_result(result):
    #title = ["code", "name", "open", "close", "now", "high", "low","open(%)", "now(%)","high(%)","low(%)", "swing(%)"]
    title = ["代码", "名称", "今开", "昨收", "现价", "最高", "最低","今开(%)", "现价(%)","最高(%)","最低(%)", "振幅(%)"]
    print_to_console(title, 0)
    data_line = []
    key_temp = ''
    color = 2  # 1 : red; 2 : blue
    
    for code in result:
        data_line.append(code)
        for key in result[code]:
            if key.find("precent", 0, len(key)) != -1:
                key_temp = str(result[code][key]) + "%"
            else:
                key_temp = str(result[code][key])
            data_line.append(key_temp)
            
            if key == "now_precent":
                if result[code][key] >= float(0.01):
                    color = 1
                else:
                    color = 2
            else:
                pass
        print_to_console(data_line, color)
        data_line = []

def clear_console():
    command ='clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def start_real_market():
    while True:
        real = get_care_real_data()
        result = deal_stock_data(real)
        print_result(result)
        time.sleep(3)
        clear_console()

def main():
    timer = threading.Timer(5, start_real_market)
    timer.start()
 


if __name__ == "__main__":
    main()