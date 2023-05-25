#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/3/4 20:14
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import logging
import os
import Common.config as conf

"""
log_path = conf.get_value('')
if not os.path.exists(log_path):
    os.mkdir(log_path)
"""


class Logger(object):

    def __init__(self, logger):
        try:

            self.logger = logging.getLogger(logger)
            self.logger.setLevel(logging.DEBUG)
        except Exception as e:
            raise e
        """
        # pytest报告可以自动将log整合进报告，不用再自己单独设置保存
        if not self.logger.handlers:
            # 格式化处理器
            formatter = logging.Formatter(fmt="%(asctime)s - [%(filename)s - %(funcName)s] - [line:%(lineno)d] - %(levelname)s: %(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")
            # 文件处理器
            self.fh = logging.FileHandler(self.log_name, mode='a', encoding='utf-8')
            self.fh.setLevel(logging.DEBUG)
            self.logger.addHandler(self.fh)
            # 控制台处理器
            self.sh = logging.StreamHandler()
            self.sh.setLevel(logging.DEBUG)
            self.logger.addHandler(self.sh)

            self.fh.setFormatter(formatter)
            self.sh.setFormatter(formatter)
        """

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)


"""
logger = Logger().logger
"""