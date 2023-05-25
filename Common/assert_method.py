#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time     : 2022/3/10 15:45
# @Author   : Li Hanqing
# @Email    : 1430066373@qq.com

import logging
from Common.basepage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger('test.assert_method')

class AssertMethod(BasePage):

    def isSelected(self, locator):
        '''

        :param locator:
        :return: 判断元素是否被选中，返回bool值
        '''
        ele = self.get_element(locator)
        r = ele.is_selected()
        return r

    def isElementExist(self, locator):
        '''

        :param locator:
        :return: 判断元素是否存在x
        '''
        log.info("判断元素{}是否存在".format(locator))
        try:
            self.get_element(locator)
            log.info("元素{}存在".format(locator))
            return True
        except:
            self.screenshot()
            log.error("元素{}不存在".format(locator))
            return False

    def is_title(self, _title=''):
        '''

        :param _title: 文本
        :return: 判断标题是否为x，返回bool
        '''
        log.info("判断标题是否为：" + _title)
        try:
            result = WebDriverWait(self.driver, self.timeout, self.poll_frequency).until(EC.title_is(_title))
            log.info("标题为：" + _title)
            return result
        except:
            self.screenshot()
            log.error("标题不是：" + _title)
            return False

    def is_title_contains(self, _title=''):
        '''

        :param _title: 文本
        :return: 判断标题是否包含文本x，返回bool值
        '''
        log.info("判断标题是否包含文本：" + _title)
        try:
            result = WebDriverWait(self.driver, self.timeout, self.poll_frequency).until(EC.title_contains(_title))
            log.info("标题包含：" + _title)
            return result
        except:
            self.screenshot()
            log.info("标题不包含：" + _title)
            return False

    def is_text_in_element(self, locator, _text=''):
        '''

        :param locator:
        :param _text: 文本
        :return: 判断元素文本是否为x，返回bool值
        '''
        log.info("判断元素文本是否为：" + _text)
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.poll_frequency).until(
                EC.text_to_be_present_in_element(locator, _text))
            log.info("元素文本为：" + _text)
            return result
        except:
            self.screenshot()
            log.error("元素文本不为：" + _text)
            return False

    def is_value_in_element(self, locator, _value=''):
        '''

        :param locator:
        :param _value:
        :return: 判断元素value值是否为x，返回bool值, 如果value为空字符串，返回Fasle
        '''
        log.info("判断元素value值是否为：" + _value)
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.poll_frequency).until(
                EC.text_to_be_present_in_element_value(locator, _value))
            log.info("元素value值为：" + _value)
            return result
        except:
            self.screenshot()
            log.error("元素value值不为：" + _value)
            return False

    def is_alert(self, timeout=3):
        '''

        :param timeout: 延迟时间
        :return: 判断是否存在alert，存在则返回alert实例，不存在则返回false
        '''
        log.info("判断是否存在alert，并返回alert实例")
        try:
            result = WebDriverWait(self.driver, timeout, self.poll_frequency).until(EC.alert_is_present())
            log.info("存在alert，返回实例：" + result)
            return result
        except:
            self.screenshot()
            log.error("不存在alert")
            return False