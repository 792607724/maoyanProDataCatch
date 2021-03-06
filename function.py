# coding = utf8
import gc
import logging
import os
import sys
import traceback

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
        """
        Function init method
        :param device:deliver a device reference into init method
        :param poco:deliver a poco reference into init method
        """
        self.device = device
        self.poco = poco
        # current package name
        self.package_name = "com.sankuai.moviepro"
        # current package path
        self.package_path = "./apk/maoyanPro.apk"
        # guide name text
        self.guide_name = "同意并继续"
        # function name text
        self.function_name = "排片上座"
        # your date from
        # need modified
        # self.date = "2015年4月1日"
        self.date = "2022年3月22日"
        # your date to
        # need modified
        self.goal_date = "2022年3月24日"

    def launch_maoyanPro(self):
        """
        launch maoyanPro app
        :return: no return
        """
        self.device.start_app(self.package_name)

    def skip_guide(self):
        """
        skip the first boot's guide popup window
        :return: no return
        """
        try:
            self.poco(text=self.guide_name).wait().click()
            # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
            sleep(0.5)
        except Exception as ex:
            print("No need skip guide: exception\n {}".format(str(ex)))
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    def enter_function(self):
        """
        enter specific function:排片上座
        :return:
        """
        try:
            self.poco(text=self.function_name).wait().click()
            # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
            sleep(0.5)
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    def get_current_date(self):
        """
        get current date display in the page - 排片上座
        :return: return current date in page
        """
        try:
            current_date = self.poco("com.sankuai.moviepro:id/tv_date").wait().get_text()
            sleep(0.5)
            print(current_date)
            return current_date
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    def wait_to_goal_date(self):
        """
        wait you manually choose the goal date you want start from
        :return: if choose the current date is the goal date will return True or you need choose the correct date ,catch data program will begin
        """
        try:
            self.poco("com.sankuai.moviepro:id/tv_date").wait().click()
            sleep(0.5)
            print("Please choose your date by manually:\n{}".format(self.date))
            while True:
                try:
                    choose_date = self.get_current_date()
                    print("Waiting…… now please scroll to find specific date……")
                    if choose_date == self.date:
                        print("Date choose correct, start catch data")
                        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
                        del choose_date
                        gc.collect()
                        return True
                    sleep(1)
                except Exception:
                    exc_type, exc_value, exc_obj = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)
                    continue
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    def catch_data(self):
        """
        catch data method to transfer save_data_when_scrill method to begin test and return data
        :return: return the catching data from current page
        """
        try:
            current_day_data = self.save_data_when_scroll()
            return current_day_data
        except Exception as ex:
            print("No need do this, check your code exception\n {}".format(str(ex)))
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    def save_data_when_scroll(self):
        """
        save data when scroll to save each days data and return to deal with
        :return:return current page data
        """

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

        if scroll_head.exists():
            try:
                while not scroll_tail.exists():
                    # situation 1
                    if scroll_head.exists() and ll_root.exists():
                        # 获取数据
                        self.get_data_situation_1()
                        # 判断当前网络OK
                        self.network_reset_operate()
                        common.scroll_up_down(percent=0.6, duration=1)
                    # situation 2
                    elif (not scroll_head.exists()) and ll_root.exists():
                        # 获取数据
                        self.get_data_situation_2()
                        # 判断当前网络OK
                        self.network_reset_operate()
                        common.scroll_up_down(percent=0.6, duration=1)
                # situation 2
                if scroll_tail.exists():
                    # 判断当前网络OK
                    self.network_reset_operate()
                    # 获取数据
                    self.get_data_situation_1()
                    print("已到底部，当天数据获取完毕")
            except Exception as ex:
                print("No need do this, check your code exception\n {}".format(str(ex)))
                exc_type, exc_value, exc_obj = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)
        return data_temp

    def network_reset_operate(self):
        # # 显示网络连接问题时，点击下page即可刷新继续测试
        no_network_refresh = self.poco(text="数据获取失败，请检查网络后刷新")
        while no_network_refresh.wait().exists():
            no_network_refresh.click()
            no_network_refresh.invalidate()
            print("Refresh page, current network error, please check your network!")
            sleep(3)

    # situation 1
    def get_data_situation_1(self):
        """
        situation 1:to emulate the situation when last display is not whole movie list that means exists other elements
        :return:no return just 1 situation to compatible all possible happened
        """
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
                    data_temp.append(data_temp_item)
                    return
                # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
                del tv_name, tv_rate, tv_count
                gc.collect()
            except Exception as ex:
                print("Maybe need check this error:\n{}".format(str(ex)))
                exc_type, exc_value, exc_obj = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)
                continue
        data_temp.append(data_temp_item)
        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
        del children_number
        gc.collect()

    # situation 2
    def get_data_situation_2(self):
        """
            situation 2:to emulate the situation when last display is whole movie list that means not exists other elements
            :return:no return just 1 situation to compatible all possible happened
        """
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
                # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
                del tv_name, tv_rate, tv_count
                gc.collect()
            except Exception as ex:
                print("Maybe need check this error:\n{}".format(str(ex)))
                exc_type, exc_value, exc_obj = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)
                continue
        data_temp.append(data_temp_item)
        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
        del children_number
        gc.collect()

    def catchDataProcess(self):
        """
        Main catch data process in their
        :return: no return , data deal with will generate excel file and append each days,
        if all process from self.date to self.goal_date, program will stop that means all data catch finished
        """
        next_day = poco("com.sankuai.moviepro:id/tv_next").wait()
        # judge current page is the self.date to start from
        if function.wait_to_goal_date():
            self.network_reset_operate()
            print("Begin")
            # a mark for the cycle up to self.goal_date
            finished = False
            # 先创建excel表格
            # customized excel data file name, you can change it as you wish
            filename = "./result/MovieDataFrom{}To{}.xlsx".format(self.date, self.goal_date)
            common.create_excel(filename)
            # into the data catching cycle
            while not finished:
                # # 显示网络连接问题时，点击下page即可刷新继续测试
                self.network_reset_operate()

                # 无排片数据时进入下一天
                # compatible the situation when some page has no data will filled with [["当天无排片", "已跳过", "当天无排片"]]
                while self.poco(text="暂无排片数据").wait().exists():
                    print("暂无排片数据，当前页面开始跳过！")
                    # deliver current time、data、excel file name to append data file in excel
                    self.generateDataToExcel(self.get_current_date(), [["当天无排片", "已跳过", "当天无排片"]], filename)
                    sleep(2)
                    next_day.invalidate()
                    next_day.click()
                    if self.get_current_date() == self.goal_date:
                        print("数据获取已结束！")
                        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
                        del next_day
                        gc.collect()
                        return

                # 获取当前页面(当天)数据
                current_page_date = self.get_current_date()
                # deliver current time、data、excel file name to append data file in excel
                sleep(2)
                self.generateDataToExcel(current_page_date, function.catch_data(), filename)
                while True:
                    try:
                        next_day.invalidate()
                        if next_day.exists():
                            # if current date is the goal date, break cycle, program done
                            if function.get_current_date() == function.goal_date:
                                finished = True
                                # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
                                del next_day, current_page_date
                                gc.collect()
                                break
                            next_day.invalidate()
                            next_day.click()
                            break
                        else:
                            # scroll up use -0.6, sleep 3s will make sure the screen stable after the refresh when scroll
                            self.network_reset_operate()
                            common.scroll_up_down(percent=-0.6, duration=1)
                            sleep(3)
                    except Exception:
                        self.network_reset_operate()
                        common.scroll_up_down(percent=-0.6, duration=1)
                        sleep(3)
                        exc_type, exc_value, exc_obj = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)

    # 测一天写一天
    def generateDataToExcel(self, current_page_date, data, filename):
        """
        transfer the write into excel method to append each day's data and write into excel file
        :param current_page_date: current page's date
        :param data: deliver current page's data
        :param filename: deliver the excel file path+name you want to append
        :return: no return
        """
        print("Begin generate excel data:\n{}".format(filename))
        common.write_into_excel(current_page_date, data=data, filename=filename)


if __name__ == '__main__':
    """
    Main program work flow
    1、device:connect to device
    2、poco:generate a poco selector for current deivce
    3、function:init Function class and deliver device、poco into it
    4、common:init Common class and deliver device、poco into it
    """
    try:
        print(
            "==================================================Main Process "
            "Run==================================================")

        # need modified
        # device = connect_device("Android:///{}".format("7c2440fd"))
        device = connect_device("Android:///{}".format("127.0.0.1:7555"))
        # device = connect_device("Android:///{}".format("emulator-5554"))
        poco = AndroidUiautomationPoco(device=device, use_airtest_input=False, screenshot_each_action=False)
        poco().exists()
        function = Function(device, poco)

        common = Common(device, poco)
        # install maoyanPro apk
        common.install_apk(function.package_path)
        # grant all permission for maoyanPro app
        common.grantPermission(function.package_name)
        # launch maoyanPro
        function.launch_maoyanPro()
        # skip maoyanPro's first skip guide
        function.skip_guide()
        # enter maoyanPro's main function:排片上座
        function.enter_function()
        # Beign catch data process to extract data by automatically UI work flow
        function.catchDataProcess()
    except Exception as ex:
        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
        print("Main Process happened exception, please check it:\n{}".format(str(ex)))
        function.network_reset_operate()
        common.scroll_up_down(percent=-0.6, duration=1)
        common.scroll_up_down(percent=-0.6, duration=1)
        sleep(3)
        current_date = function.get_current_date()
        print("Current date is:{}".format(current_date))
        if not os.path.exists("./Error"):
            os.mkdir("./Error")
            print("Create folder success")
        with open("./Error/{}.log".format(current_date), "w") as error_log:
            error_log.writelines(
                "Current date is {}, and Main Process happened exception, please check it:\n{}".format(current_date,
                                                                                                       str(ex)))
            error_log.close()
        PocoServicePackage = 'com.netease.open.pocoservice'
        os.system("adb shell am start -n {}/.TestActivity".format(PocoServicePackage))
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_obj, limit=2, file=sys.stdout)
    finally:
        # 尝试滞空，是否能修复内存泄漏问题 -- Guangtao
        del device, poco, function, common
        gc.collect()
        print(
            "==================================================Main Process "
            "Done==================================================")
