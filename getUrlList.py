
# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

'getCityURL Method'

__author__ = 'WangZhe'

import urllib.request
from bs4 import BeautifulSoup
import configparser
import codecs


def getUrl():
    cf = configparser.ConfigParser()
    cf.readfp(codecs.open("config.ini", "r", "utf-8-sig"))

    # db config
    host = cf.get("MySQL", "host")
    port = cf.get("MySQL", "port")
    dataBase = cf.get("MySQL", "dataBase")
    userName = cf.get("MySQL", "userName")
    password = cf.get("MySQL", "password")
    raise_on_warnings = cf.getboolean("MySQL", "raise_on_warnings")

    config = {
        'user': userName,
        'password': password,
        'host': host,
        'database': dataBase,
        'raise_on_warnings': raise_on_warnings
    }

    # condition
    begin_year = cf.getint("TIME_SCOPE", "BEGIN_YEAR")
    begin_month = cf.getint("TIME_SCOPE", "BEGIN_MONTH")
    begin_day = cf.getint("TIME_SCOPE", "BEGIN_DAY")
    end_year = cf.getint("TIME_SCOPE", "END_YEAR")
    end_month = cf.getint("TIME_SCOPE", "END_MONTH")
    end_day = cf.getint("TIME_SCOPE", "END_DAY")

    flag = cf.getint("CITY", "FLAG")
    cityList = []
    if flag == 0:
        cityList = cf.get("CITY", "CITY").split(',')
    else:
        page = urllib.request.urlopen('http://www.tianqihoubao.com/lishi/henan.htm')
        htmlStr = page.read().decode('utf-8')
        soup = BeautifulSoup(htmlStr, features='lxml')
        #     print(soup.prettify())
        dd = soup.find_all('dd')
        i = 0
        for city in dd:
            i += 1
            town = city.find_all('a')
            j = 0
            for a in town:
                j += 1
                if (i == 2) & (j == 2):
                    continue
                else:
                    cityList.append(a['href'].replace("/lishi/", "").replace(".html", ""))

    # time_scope
    time_scope = []

    while True:
        if begin_month < 10:
            time_scope.append(str(begin_year) + "0" + str(begin_month))
        else:
            time_scope.append(str(begin_year) + str(begin_month))
        if (begin_year == end_year) and (begin_month == end_month):
            break
        begin_month += 1
        if begin_month == 13:
            begin_month = 1
            begin_year += 1

    # print(time_scope)

    urlList = []
    for city in cityList:
        url = []
        for time in time_scope:
            url.append("http://www.tianqihoubao.com/lishi/"+city+"/month/"+time+".html")
        urlList.append(url)

    result = []
    result.append(config)
    result.append(urlList)
    result.append(begin_day)
    result.append(end_day)
    print(result)
    return result


if __name__ == '__main__':
    getUrl()
