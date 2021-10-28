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
        self.device = device
        self.poco = poco

    def install_apk(self, package_path="./apk/maoyanPro.apk"):
        print("begin install app:{}".format(package_path))
        self.device.install_app(filepath=package_path, replace=True)

    def grantPermission(self, package_name="com.sankuai.moviepro"):
        for i in range(2):
            try:
                permission_list = self.device.shell(
                    "dumpsys package {} | grep permission | grep granted=false".format(package_name))
                sleep(3)
                permission_list = re.findall("\s*(.*):\sgranted", permission_list)
                print("current app:{} has permission:[{}]".format(package_name, permission_list))
                if permission_list:
                    for permission in permission_list:
                        self.device.shell("pm grant {} {}".format(package_name, permission))
                        print("Now, grant app {} - permission {}".format(package_name, permission))
            except AdbShellError as ex:
                print("No need granted for this permission!")
                print(str(ex))

    def scroll_up_down(self, percent=0.6, duration=1):
        print("Beign scroll……")
        self.poco.scroll(direction="vertical", percent=percent, duration=duration)
        sleep(1)

    def create_excel(self, filename):
        if not os.path.exists("./result"):
            os.system("mkdir ./result")
        file_path = "{}".format(filename)
        df = pd.DataFrame(columns=["日期", "电影名称", "场次占比", "场次"])
        df.to_excel(file_path, index=False)
        print("{}文件创建成功".format(filename))

    def write_into_excel(self, data, filename):
        df = pd.read_excel(filename, header=None, engine="openpyxl")
        ds = pd.DataFrame([["1", "2", "3", "4"]])
        df = df.append(ds, ignore_index=True)
        df.to_excel(filename, index=False, header=False)
        print(str(data) + "\n")
