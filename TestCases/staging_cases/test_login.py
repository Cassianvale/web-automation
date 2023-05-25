#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2023/03/22 17:11
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import pytest
from Common import config as conf
from PageObject.staging.login_page import LoginPage
import logging


log = logging.getLogger('test.Login')


class Test_Login():

    # 导入selenium驱动
    driver = conf.get_value('driver')
    login_page = LoginPage(driver)

    def test_open_login(self):
        """打开登录页面"""
        # 断言title是否正确
        try:
            self.login_page.open_loginpage()
            self.login_page.sleep(1)
            # 如果正确返回result，如果错误返回False
            self.login_page.title_contains(expect_contain_text='热铁盒123')
            log.info('断言title成功，网页被成功打开')
        except Exception as e:
            self.login_page.screenshot('断言失败，网页打开失败')
            raise e

    def test_sendkeys(self):
        """登录提交校验"""
        try:
            self.login_page.input_username('1430066373@qq.com')
            self.login_page.sleep(1)
            self.login_page.input_password('z82190464')
            self.login_page.sleep(1)
            log.info("输入用户名密码成功")
            self.login_page.click_sumbit
            log.info("提交登录")
        except Exception as e:
            self.login_page.screenshot('输入用户名密码失败')
            raise e

    def test_sumbit(self):
        '''登录校验'''
        try:
            self.login_page.click_sumbit()
            self.login_page.sleep(1)
            assert self.login_page.get_current_url() =='https://account.retiehe.com/'
        except Exception as e:
            self.login_page.screenshot('登录失败，请检查登录页面')
            raise e
            
if __name__ == '__main__':
    # pytest.main(['-v', '-s', 'test_home.py::TestHome::test_input_keyword'])
    pytest.main(['-v', '-s'])