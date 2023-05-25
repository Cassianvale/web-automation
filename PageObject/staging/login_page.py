#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2023/03/22 17:09
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import Common.config as conf
import logging
from Common.basepage import BasePage

log = logging.getLogger('test.login_page')


class LoginPage(BasePage):

    def __init__(self,driver):

        super().__init__(driver)

    # i=输入框,b=按钮,l=链接,a=Alert弹窗,im=图片,t=文字控件,d=div,lab=label
    # 用户名输入框
    i_username = "xpath,//input[@name='email']"
    # 密码输入框
    i_password = "xpath,//input[@name='password']"
    # 登录按钮
    b_sumbit = "xpath,//button[text()='登录']"

    def open_loginpage(self):
        # 从全局变量取默认的staging环境地址
        site = conf.get_value('site')
        self.open(site)

    # 输入用户名
    def input_username(self, keys=None):
        self.type(self.i_username, keys)

    # 输入密码
    def input_password(self, keys=None):
        self.type(self.i_password, keys)

    # 点击提交登录
    def click_sumbit(self):
        self.click(self.b_sumbit)