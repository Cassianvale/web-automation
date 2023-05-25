#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/5/16 0:07
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import os
from Common.read_data import data
from selenium import webdriver


def init():
    global _global_dict
    _global_dict = {}

    # 代码根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 当前程序所在目录
    _global_dict['root_path'] = root_dir
    # 存放截图
    _global_dict['screenshot_path'] = "{}/File/screenshot/".format(root_dir)
    # 下载文件夹
    _global_dict['download_path'] = "{}/File/download/".format(root_dir)
    # 上传文件夹
    _global_dict['upload_path'] = "{}/File/upload/".format(root_dir)
    # 存放报告路径
    _global_dict['report_path'] = "{}/File/report/".format(root_dir)

    # 保存driver
    _global_dict['driver'] = None

    # 设置运行环境网址主页，run中设置
    _global_dict['site'] = 'https://account.retiehe.com/'

    # 运行环境，默认staging，可设为preprod
    _global_dict['environment'] = 'staging'


def set_value(name, value):
    """
    修改全局变量的值
    :param name: 变量名
    :param value: 变量值
    """
    _global_dict[name] = value


def get_value(name, def_value='no_value'):
    """
    获取全局变量的值
    :param name: 变量名
    :param def_value: 默认变量值
    :return: 变量存在时返回其值，否则返回'no_value'
    """
    try:
        return _global_dict[name]
    except KeyError:
        return def_value

if __name__ == '__main__':
    init()
