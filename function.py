# coding = utf8
import logging
import os

from common import Common

os.path.abspath(".")
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    @File:function.py
    @Author:Bruce
    @Date:2021/10/27
"""

if __name__ == '__main__':
    print("Running test……")
    package_name = "com.sankuai.moviepro"
    device = connect_device("Android:///{}".format("7c2440fd"))
    poco = AndroidUiautomationPoco(device=device, use_airtest_input=False, screenshot_each_action=False)
    common = Common(device, poco)
    common.grantPermission(package_name)
