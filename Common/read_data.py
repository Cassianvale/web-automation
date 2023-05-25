#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/5/19 21:00
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import yaml, logging
from Common import config as conf
from configparser import ConfigParser


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:

    @staticmethod
    def load_yaml(filepath):
        """
        加载yaml文件
        :param filepath: 文件路径
        """
        # try:
        #     with open(filepath, 'r', encoding='utf-8') as f:
        #         value = yaml.safe_load(f.read(stream=f))
        #         data = list(value.values())
        #         logging.info("读取数据成功！正在加载 ==>> {} ".format(filepath))
        #         return data
        # except Exception as e:
        #     logging.error(f"文件打开错误，错误信息：{e}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f.read())
                logging.info("读取数据成功！正在加载 ==>> {} ".format(filepath))
                return data
        except Exception as e:
            logging.error(f"文件打开错误，错误信息：{e}")


data = ReadFileData