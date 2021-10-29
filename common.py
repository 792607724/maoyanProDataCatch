# coding = utf8
import os
import re
import time
from time import sleep

import pandas as pd
from airtest.core.error import AdbShellError

os.path.abspath(".")
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    @File:common.py
    @Author:Bruce
    @Date:2021/10/27
"""


class Common:

    def __init__(self, device, poco):
        """
        Common init method
        :param device:deliver a device reference into init method
        :param poco:deliver a poco reference into init method
        """
        self.device = device
        self.poco = poco

    def install_apk(self, package_path="./apk/maoyanPro.apk"):
        """
        install maoyanPro apk
        :param package_path:deliver the apk's saving path
        :return: no return
        """
        print("begin install app:{}".format(package_path))
        self.device.install_app(filepath=package_path, replace=True)

    def grantPermission(self, package_name="com.sankuai.moviepro"):
        """
        grant app permission
        :param package_name:deliver a package name which you want grant all permission
        :return: no return
        """
        # run twice for make sure when the app installed first will not be complete granted
        for i in range(2):
            try:
                # first:dump current package's permission which is not granted
                permission_list = self.device.shell(
                    "dumpsys package {} | grep permission | grep granted=false".format(package_name))
                sleep(3)
                # deal with the permission_list and filter all permission append to a list
                permission_list = re.findall("\s*(.*):\sgranted", permission_list)
                print("current app:{} has permission:[{}]".format(package_name, permission_list))
                if permission_list:
                    for permission in permission_list:
                        # grant each permission for current package
                        self.device.shell("pm grant {} {}".format(package_name, permission))
                        print("Now, grant app {} - permission {}".format(package_name, permission))
            except AdbShellError as ex:
                print("No need granted for this permission!")
                print(str(ex))

    def scroll_up_down(self, percent=0.6, duration=1):
        """
        scroll screen up and down
        :param percent: control the scroll distance and direction
        :param duration:control the scroll time
        :return:
        """
        print("Beign scroll……")
        self.poco.scroll(direction="vertical", percent=percent, duration=duration)
        sleep(1)

    def create_excel(self, filename):
        """
        create excel by absolute file path and name
        :param filename:deliver a filename for create
        :return: no return
        """
        if not os.path.exists("./result"):
            os.mkdir("./result")
            print("Create folder success")
        file_path = "{}".format(filename)
        df = pd.DataFrame(columns=["日期", "电影名称", "场次占比", "场次"])
        df.to_excel(file_path, index=False)
        print("{} file create success!".format(filename))

    def write_into_excel(self, current_page_date, data, filename):
        """
        this method use to append data into a exists excel file
        :param current_page_date:deliver current page date for data generate
        :param data:deliver current page date to append
        :param filename:the excel file you create by create_excel method
        :return:
        """
        df = pd.read_excel(filename, header=None, engine="openpyxl")
        print(data)
        # [['当天无排片，已跳过']]
        b = data[0]
        # 按这个格式处理数据并传入，每天的都追加进去
        n = 0
        temp_list = []
        while n < len(b):
            list_temp = []
            print(len(b))
            list_temp.append(current_page_date)
            # catching data from app all in one list,three data is a movie's data, cycle it to extract each movie's data
            for n in range(n, n + 3):
                list_temp.append(b[n])
            n += 1
            temp_list.append(list_temp)
        print(temp_list)
        ds = pd.DataFrame(temp_list)
        df = df.append(ds, ignore_index=True)
        df.to_excel(filename, index=False, header=False)
        print(str(data) + "\n")
