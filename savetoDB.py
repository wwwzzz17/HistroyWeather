# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

'savetoDB Method'

__author__ = 'WangZhe'

import sys
import mysql.connector
from mysql.connector import errorcode
import re


def save(dataList, table_name, config):

    try:
        # print(config)
        conn = mysql.connector.connect(**config)

        cursor = conn.cursor()
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        a = [re.sub("'", '', each) for each in table_list]
        # print(table_list)
        if table_name not in a:
            cursor.execute("CREATE TABLE " + table_name + """
                                (
                                    `ID` varchar(128) COLLATE utf8_unicode_ci NOT NULL COMMENT 'UUID',
                                    `DATE` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '时间',
                                    `D_WEATHER` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '日间天气',
                                    `N_WEATHER` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '夜间天气',
                                    `D_TEMPERATURE` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '日间气温(摄氏度)',
                                    `N_TEMPERATURE` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '夜间气温(摄氏度)',
                                    `D_WINDYDIRECTION` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '日间风向',
                                    `N_WINDYDIRECTION` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '夜间风向',
                                    `UPDATE_TIME` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
                                    PRIMARY KEY (`ID`)
                                  ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_general_ci;

                    """)
        sql = "insert into " + table_name + " (ID, DATE, D_WEATHER, N_WEATHER, D_TEMPERATURE, N_TEMPERATURE, D_WINDYDIRECTION, N_WINDYDIRECTION) value (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, dataList)
        # data = cursor.fetchone()
        # cursor.execute("select * from ZHENGZHOU")
        # data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        # print(data)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return 1


if __name__ == '__main__':
    save(sys.argv[0], sys.argv[1], sys.argv[2])
