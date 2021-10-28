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
        self.date = "2021年10月28日"
        self.goal_date = "2021年10月29日"

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

    def wait_to_goal_date(self):
        try:
            self.poco("com.sankuai.moviepro:id/tv_date").wait().click()
            print("Please choose your date by manually:\n{}".format(self.date))
            while True:
                try:
                    choose_date = self.get_current_date()
                    print("Waiting…… now please scroll to find specific date……")
                    if choose_date == self.date:
                        print("Date choose correct, start catch data")
                        return True
                    sleep(1)
                except Exception:
                    continue
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))

    def catch_data(self):
        try:
            current_day_data = self.save_data_when_scroll()
            return current_day_data
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))

    def save_data_when_scroll(self):
        global data_temp, data_temp_item
        data_temp = []
        data_temp_item = []
        """
        先判断是否存在"影视作品《免责说明》"：
            存在：不需要滚动，直接获取数据
            不存在：
                1、如果scroll_head = self.poco(text="片名").wait()且ll_root = self.poco("com.sankuai.moviepro:id/ll_root").wait()存在：
                    获取root_recycle = self.poco("com.sankuai.moviepro:id/root_recycle").wait()有多少个children
                    从第三个到最后一个开始获取当前界面的所有children，
                        获取片名 - 场次占比 - 场次，拼接数据
                2、如果scroll_head = self.poco(text="片名").wait()不存在且ll_root = self.poco("com.sankuai.moviepro:id/ll_root").wait()存在：
                    获取root_recycle = self.poco("com.sankuai.moviepro:id/root_recycle").wait()有多少个children
                    从第二个到最后一个开始获取当前界面的所有children，
                        获取片名 - 场次占比 - 场次，拼接数据
                每次滚动获取完数据都判断一次"影视作品《免责说明》"是否存在：
                    存在：则完成这一天获取
                    不存在：继续滚动获取
        该函数用于判断截取数据并返回给catch_data函数
        """
        scroll_head = self.poco(text="片名").wait()
        scroll_tail = self.poco(text="影视作品《免责说明》").wait()
        ll_root = self.poco("com.sankuai.moviepro:id/ll_root").wait()
        root_recycle = self.poco("com.sankuai.moviepro:id/root_recycle").wait()
        next_day = self.poco(text="后一天").wait()

        if scroll_head.exists():
            try:
                while not scroll_tail.exists():
                    # situation 1
                    if scroll_head.exists() and ll_root.exists():
                        # 获取数据
                        self.get_data_situation_1()
                        common.scroll_up_down(percent=0.6, duration=1)
                    # situation 2
                    elif (not scroll_head.exists()) and ll_root.exists():
                        # 获取数据
                        self.get_data_situation_2()
                        common.scroll_up_down(percent=0.6, duration=1)
                # situation 2
                if scroll_tail.exists():
                    # 获取数据
                    self.get_data_situation_1()
                    print("已到底部，当天数据获取完毕")
            except Exception as ex:
                print("No need do this, check your code exception\n {}".format(str(ex)))
        return data_temp

    # situation 1
    def get_data_situation_1(self):
        root_recycle = self.poco("com.sankuai.moviepro:id/root_recycle")
        children_number = len(root_recycle.children())
        print(children_number)
        for i in range(2, children_number):
            try:
                tv_name = root_recycle.children()[i].children().children().children().child(
                    "com.sankuai.moviepro:id/tv_name").get_text()
                tv_rate = root_recycle.children()[i].children().child("com.sankuai.moviepro:id/tv_rate").get_text()
                tv_count = root_recycle.children()[i].children().child("com.sankuai.moviepro:id/tv_count").get_text()
                print("{} - {} - {}".format(tv_name, tv_rate, tv_count))
                if tv_name not in data_temp_item:
                    data_temp_item.append(tv_name)
                    data_temp_item.append(tv_rate)
                    data_temp_item.append(tv_count)
                if tv_name == "其它":
                    print("数据获取完成")
                    return
            except Exception as ex:
                print("Maybe need check this error:\n{}".format(str(ex)))
                continue
        data_temp.append(data_temp_item)

    # situation 2
    def get_data_situation_2(self):
        root_recycle = self.poco("com.sankuai.moviepro:id/root_recycle")
        children_number = len(root_recycle.children())
        print(children_number)
        for i in range(0, children_number):
            try:
                tv_name = root_recycle.children()[i].children().children().children().child(
                    "com.sankuai.moviepro:id/tv_name").get_text()
                tv_rate = root_recycle.children()[i].children().child("com.sankuai.moviepro:id/tv_rate").get_text()
                tv_count = root_recycle.children()[i].children().child("com.sankuai.moviepro:id/tv_count").get_text()
                print("{} - {} - {}".format(tv_name, tv_rate, tv_count))
                if tv_name not in data_temp_item:
                    data_temp_item.append(tv_name)
                    data_temp_item.append(tv_rate)
                    data_temp_item.append(tv_count)
                if tv_name == "其它":
                    print("数据获取完成")
                    return
            except Exception as ex:
                print("Maybe need check this error:\n{}".format(str(ex)))
                continue
        data_temp.append(data_temp_item)

    def catchDataProcess(self):
        # data_list = []
        next_day = poco(text="后一天").wait()
        if function.wait_to_goal_date():
            print("Begin")
            finished = False
            while not finished:
                # 获取当前页面(当天)数据
                # data_list.append(function.catch_data())
                self.generateDataToExcel(function.catch_data())
                while True:
                    try:
                        next_day.invalidate()
                        if next_day.exists():
                            if function.get_current_date() == function.goal_date:
                                finished = True
                                break
                            next_day.click()
                            break
                        else:
                            common.scroll_up_down(percent=-0.6)
                    except Exception:
                        common.scroll_up_down(percent=-0.6)

    # 测一天写一天
    def generateDataToExcel(self, data):
        filename = "{}MovieDataFrom{}To{}.xlsx".format(cur_time, self.date, self.goal_date)
        print("Begin generate excel data:\n{}".format(filename))
        common.write_into_excel(data=data, filename=filename)


if __name__ == '__main__':
    print("Running test……")

    device = connect_device("Android:///{}".format("7c2440fd"))
    poco = AndroidUiautomationPoco(device=device, use_airtest_input=False, screenshot_each_action=False)

    function = Function(device, poco)

    common = Common(device, poco)
    common.install_apk(function.package_path)
    common.grantPermission(function.package_name)

    function.launch_maoyanPro()
    function.skip_guide()
    function.enter_function()
    function.catchDataProcess()
