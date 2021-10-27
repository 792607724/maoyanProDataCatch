# coding = utf8
import os
import re

os.path.abspath(".")
"""
    @File:common.py
    @Author:Bruce
    @Date:2021/10/27
"""


class Common:

    def __init__(self, device, poco):
        self.device = device
        self.poco = poco

    def grantPermission(self, package_name="com.sankuai.moviepro"):
        permission_list = self.device.shell(
            "dumpsys package {} | grep permission | grep granted=false".format(package_name))
        permission_list = re.findall("\s*(.*):\sgranted", permission_list)
        print("current app:{} has permission:[{}]".format(package_name, permission_list))
        for permission in permission_list:
            self.device.shell("pm grant {} {}".format(package_name, permission))
            print("Now, grant app {} - permission {}".format(package_name, permission))
