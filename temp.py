# coding = utf8
import os

from rich import print

os.path.abspath(".")
"""
    @File:temp.py
    @Author:Bruce
    @Date:2021/10/29
"""


def hello():
    print("OK")


if __name__ == '__main__':
    os.system("adb devices")
    print("OK,[bold magenta]That is so exciting[/bold magenta]!", ":vampire:", locals(), "\n this is bullshit")
    os.system("adb uninstall com.netease.nie.yosemite")
    os.system("adb uninstall com.netease.open.pocoservice.test")
    os.system("adb uninstall com.netease.open.pocoservice")
    os.system("adb uninstall com.sankuai.moviepro")
