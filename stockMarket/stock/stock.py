
import easyquotation  as eq
import time, os, threading, sys, argparse

parser = argparse.ArgumentParser(description='stock market program:')
parser.add_argument('--info', '-i', help = 'show sample or detail information.', default = 'sample')
parser.add_argument('--color', '-c', help = 'show  various color.', default = 'close')
parser.add_argument('--snap', '-n', help = 'get information by snap.', default = 6)
parser.add_argument('--sort', '-o', help = 'sort list by key.', default = 'now_precent')
parser.add_argument('--cycle', '-y', help = 'get information by cycle.', default = 'close')
args = parser.parse_args()

my_stock = ['000796','300732','300205', '399006']

def get_care_real_data():
    quot = eq.use('sina')   # ['sina', 'tencent', 'qq'] 
    real_data = quot.real(my_stock)
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
    for code in stockReal:
        stock_result[code] = {}
        open = close = now = high = low = 0

        for key in stockReal[code]:
            if key == "name":
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
        high_precent = get_percent(close, high)
        stock_result[code]["high_precent"] = high_precent
        low_precent = get_percent(close, low)
        stock_result[code]["low_precent"] = low_precent
        swing_precent = get_percent(low, high)
        stock_result[code]["swing_precent"] = swing_precent
    return stock_result

# a chinese char have the length of two chars, need calc the length by ourself
def chinese_count(fields):
    counts = 0
    for _char in fields:
        if '\u4e00' <= _char <= '\u9fa5':
            counts += 1
    return counts

def print_to_console(content, color):
    result = ''
    tar_length = 10
    for val in content:
        cn_no = chinese_count(val)
        if cn_no > tar_length:
            cn_no = tar_length
        result += val.center(tar_length - cn_no, ' ')
    if args.color == 'open':
        if color == 0:
            result = '\033[34m' + result + '\033[1m'
        elif color == 1:
            result = '\033[31m' + result + '\033[1m'
        elif color == 2:
            result = '\033[0;32;40m' + result + '\033[0m'
        else:
            result = '\033[38m' + result + '\033[0m'
    else:
        result = '\033[38m' + result + '\033[0m'
    print(result)  

def get_now_precent(data_line):
    now_precent_str = ''
    if args.info != 'detail':
        now_precent_str = data_line[1]
    else:
        now_precent_str = data_line[8]
    npos = now_precent_str.find('%', 0, len(now_precent_str))
    if npos < 0:
        print("get_now_precent() failed, data_line:  ", data_line)
        return 0.0
    now_precent = round(float(now_precent_str[0:npos - 1]), 2)
    return now_precent

def sort_and_print_data(data_total):
    data_dict = {}
    for key, data_line in enumerate(data_total):
        now_precent = get_now_precent(data_line)
        data_dict[key] = now_precent
    data_sorted = sorted(data_dict.items(), key = lambda kv:(kv[1], kv[0]))
    data_sorted.reverse()
    for key, now_precent_list in enumerate(data_sorted):
        data_line = data_total[now_precent_list[0]]
        if now_precent_list[1] >= float(0.01):
            color = 1
        else:
            color = 2
        print_to_console(data_line, color)
            
def print_result(result):
    if args.info == 'detail':
        #title = ["code", "name", "open", "close", "now", "high", "low","open(%)", "now(%)","high(%)","low(%)", "swing(%)"]
        title = ["代码", "名称", "今开", "昨收", "现价", "最高", "最低","今开(%)", "现价(%)","最高(%)","最低(%)", "振幅(%)"]
    else:
        title =["名称", "涨幅(%)"]
    print_to_console(title, 0)
    data_line = []
    key_temp = ''
    color = 2  # 1 : red; 2 : blue
    data_total = []
    sort = ''
    for code in result:
        if args.info == 'detail':
            data_line.append(code)
        for key in result[code]:
            if key.find("precent", 0, len(key)) != -1:
                key_temp = str(result[code][key]) + "%"
            else:
                key_temp = str(result[code][key])
            if args.info == 'detail':
                data_line.append(key_temp)
            else:
                if key == "name" or key == 'now_precent':
                    data_line.append(key_temp)
        data_total.append(data_line)
        data_line = []
    sort_and_print_data(data_total)
        
def clear_console():
    command ='clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)
    resumme_consol_color()

#reset the default color on console
def resumme_consol_color():
    print('\033[38m' + ' ' + '\033[0m')

def start_real_market():
    while True:
        real = get_care_real_data()
        result = deal_stock_data(real)
        print_result(result)
        time.sleep(int(args.snap))
        clear_console()
        if args.cycle != 'open':
            break
    
def main():
    try:
        start_real_market()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()