#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2023/03/22 17:11
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import pytest
import Common.config as conf
from PageObject.staging.login_page import LoginPage
import logging


log = logging.getLogger('test.Login')


class Test_Login():
    """
    pytest:
    测试文件以test_开头
    测试类以Test开头，并且不能带有__init__方法
    测试函数以test_开头
    断言使用assert
    """

    driver = conf.get_value('driver')
    login_page = LoginPage(driver)
