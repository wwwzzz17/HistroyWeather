import getUrlList, savetoDB
import urllib.request
from bs4 import BeautifulSoup
import uuid
import time
import threading

timeout = []

# 定义多线程


class MyThread (threading.Thread):
    def __init__(self, name, urlList, config, begin_day, end_day):
        threading.Thread.__init__(self)
        self.name = name
        self.urlList = urlList
        self.config = config
        self.begin_day = begin_day
        self.end_day = end_day

    def run(self):
        print("Starting : ", self.name)
        timeout_list = []
        start = time.time()
        timeout.append(getData(self.name, self.urlList, timeout_list, self.config, self.begin_day, self.end_day))
        end = time.time()
        print("线程时间： ", end - start)
        print("Exiting : ", self.name)
        print(timeout)

# uuid


def gen_id():
    return uuid.uuid1()


# timeout urlList
timeout_list = []

# 爬取数据


def getData(table_name, urlList, timeout_list, config, begin_day, end_day):
    begin_day += 1
    end_day += 1

    # 城市结果集
    dataList = []

    for url in urlList:
        # print(url)
        try:
            page = urllib.request.urlopen(url, timeout=60)
            htmlStr = page.read().decode('gbk')
            soup = BeautifulSoup(htmlStr, features='lxml')

            # 地址的明文
            # title = soup.find('h1').get_text().replace(" ","").replace("\n","")
            # title = re.match(r'.+?历史天气预报', title).group()
            # name = title[:-6]
            # print(name)

            trList = soup.find_all('tr')
            # print(dataList)
            i = 0
            for tdList in trList:
                i += 1
                if i == 1:
                    continue
                elif url == urlList[0]:
                    if i >= begin_day :
                        j = 0
                        td = tdList.find_all('td')
                        itemList = []
                        itemList.append(str(gen_id()))
                        for item in td:
                            j += 1
                            if j == 1:
                                itemList.append(
                                    item.find('a').text.replace("年", "").replace("月", "").replace("日", "").replace(" ",
                                                                                                                   "").replace(
                                        "\r", "").replace("\n", ""))
                            else:
                                data = item.text.replace("\r", "").replace("\n", "").replace(" ", "").replace("℃",
                                                                                                              "").split('/')
                                itemList.append(data[0])
                                itemList.append(data[1])
                        # print(itemList)
                        savetoDB.save(itemList, table_name, config)
                        dataList.append(tuple(itemList))
                    else:
                        continue
                elif url == urlList[-1]:
                    if i <= end_day:
                        j = 0
                        td = tdList.find_all('td')
                        itemList = []
                        itemList.append(str(gen_id()))
                        for item in td:
                            j += 1
                            if j == 1:
                                itemList.append(
                                    item.find('a').text.replace("年", "").replace("月", "").replace("日", "").replace(" ",
                                                                                                                   "").replace(
                                        "\r", "").replace("\n", ""))
                            else:
                                data = item.text.replace("\r", "").replace("\n", "").replace(" ", "").replace("℃",
                                                                                                              "").split(
                                    '/')
                                itemList.append(data[0])
                                itemList.append(data[1])
                        # print(itemList)
                        savetoDB.save(itemList, table_name, config)
                        dataList.append(tuple(itemList))
                    else:
                        continue
                else:
                    j = 0
                    td = tdList.find_all('td')
                    itemList = []
                    itemList.append(str(gen_id()))
                    for item in td:
                        j += 1
                        if j == 1:
                            itemList.append(
                                item.find('a').text.replace("年", "").replace("月", "").replace("日", "").replace(" ",
                                                                                                               "").replace(
                                    "\r", "").replace("\n", ""))
                        else:
                            data = item.text.replace("\r", "").replace("\n", "").replace(" ", "").replace("℃",
                                                                                                          "").split('/')
                            itemList.append(data[0])
                            itemList.append(data[1])
                    # print(itemList)
                    savetoDB.save(itemList, table_name, config)
                    dataList.append(tuple(itemList))
        except Exception as e:
            print("url = [ "+url+" ] "+str(e))
            timeout_list.append(url)
    print(dataList)
    return timeout_list


thread_list = []
result = getUrlList.getUrl()
config = result[0]
resultURL = result[1]
begin_day = result[2]
end_day = result[3]

for urlList in resultURL:
    if urlList:
        url_name = urlList[0]
        table_name = url_name[34:-18]
        # print(table_name)
        print(urlList)
        thread = MyThread(table_name, urlList, config, begin_day, end_day)
        thread.start()
    else:
        continue

for thread in thread_list:
    thread.join()

# while True:
#     count = threading.active_count()
#     print(count)
#
#     if count == 1:
#         print("in")
#         if timeout_list:
#             for timeouturlList in timeout_list:
#                 print(timeouturlList)
#                 if len(timeouturlList):
#                     print(timeouturlList)
#                     url_name = timeouturlList[0]
#                     table_name = url_name[34:-18]
#                     print(table_name)
#                     timeout_list = getData(table_name, timeouturlList, config, begin_day, end_day)
#                     print(timeout_list)
#
#     time.sleep(10)










