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


class Function:

    def __init__(self, device, poco):
        self.device = device
        self.poco = poco
        self.package_name = "com.sankuai.moviepro"
        self.package_path = "./apk/maoyanPro.apk"
        self.guide_name = "同意并继续"
        self.function_name = "排片上座"

    def launch_maoyanPro(self):
        self.device.start_app(self.package_name)

    def skip_guide(self):
        try:
            self.poco(text=self.guide_name).wait().click()
        except Exception as ex:
            print("No need skip guide: exception\n {}".format(str(ex)))

    def enter_function(self):
        try:
            self.poco(text=self.function_name).wait().click()
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))

    def get_current_date(self):
        try:
            current_date = self.poco("com.sankuai.moviepro:id/tv_date").wait().get_text()
            print(current_date)
            return current_date
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))

    def wait_to_goal_date(self, date="2018年4月21日"):
        try:
            self.poco("com.sankuai.moviepro:id/tv_date").wait().click()
            print("Please choose your date by manually:\n{}".format(date))
            while True:
                try:
                    choose_date = self.get_current_date()
                    print("Waiting…… now please scroll to find specific date……")
                    if choose_date == date:
                        print("Date choose correct, start catch data")
                        return True
                    sleep(1)
                except Exception:
                    continue
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))

    def catch_data(self):
        try:
            scroll_head = self.poco(text="片名").wait()
            scroll_tail = self.poco(text="影视作品《免责说明》").wait()
            if scroll_head.exists():
                while True:
                    try:
                        common.scroll_up_down(percent=0.6, duration=1)
                        if scroll_tail.exists():
                            print("已到底部，当天数据获取完毕")
                    except Exception:
                        continue
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))


if __name__ == '__main__':
    print("Running test……")

    device = connect_device("Android:///{}".format("7c2440fd"))
    poco = AndroidUiautomationPoco(device=device, use_airtest_input=False, screenshot_each_action=False)

    function = Function(device, poco)

    common = Common(device, poco)
    # common.install_apk(function.package_path)
    # common.grantPermission(function.package_name)

    function.launch_maoyanPro()
    # function.skip_guide()
    function.enter_function()
    # function.get_current_date()
    # if function.wait_to_goal_date():
    #     print("Begin")
    #     function.catch_data()
    function.catch_data()
