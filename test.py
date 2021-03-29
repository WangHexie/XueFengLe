import requests
import sys

import requests
import gzip
import zlib
import json


def decompress_stream(stream):
    o = zlib.decompressobj(16 + zlib.MAX_WBITS)

    for chunk in stream:
        yield o.decompress(chunk)

    yield o.flush()


def get_latest_learning_log(cookies):
    header = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "http://web.lngqt.shechem.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://web.lngqt.shechem.cn/study",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4",
        "Cookie": f"{cookies}"

    }

    r = requests.post('http://api.lngqt.shechem.cn/webapi/learn/learnlog',
                      headers=header, stream=True)

    parseable_data = decompress_stream(r.iter_content(1024))

    full_string = ''
    for i in parseable_data:
        full_string += i.decode("utf-8")
        print(i)
    print(full_string)

    logs = json.loads(full_string)
    print(logs)
    print(logs["data"]["list"][0]["learnlist"])

    return logs["data"]["list"][0]["learnlist"]


def write_to_file(thing):
    with open("./README.md", "w", encoding="utf-8") as f:
        f.write("""# XueFengLe     

我学疯啦    

        """ + thing["title"] +"""     

        """ + str(thing))


def get_current_number():
    import datetime
    my_date = datetime.date.today()
    year, week_num, day_of_week = my_date.isocalendar()
    print("Week #" + str(week_num) + " of year " + str(year))
    return week_num


print(sys.argv[1])
cookies = sys.argv[1]

header = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "http://web.lngqt.shechem.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://web.lngqt.shechem.cn/study",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4",
    "Cookie": f"{cookies}"

}

current_lesson = get_current_number() + 35

r = requests.post('http://api.lngqt.shechem.cn/webapi/learn/addlearnlog',
                  data=f"lid={current_lesson}&token=",
                  headers=header)
print(r.content)

print(get_latest_learning_log(cookies))
write_to_file(get_latest_learning_log(cookies))
