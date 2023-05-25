#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/3/3 11:15
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import datetime
import inspect
import logging
import os
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Common import config as conf

log = logging.getLogger('test.BasePage')


# 谨慎调整
class BasePage(object):

    def __init__(self,driver=None,timeout=None, poll_frequency=None):
        if driver == None:
            self.driver = conf.get_value('driver')
        else:
            self.driver=driver
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self.wait = None

    def set_wait(self):
        self.wait = WebDriverWait(self.driver, self.timeout, self.poll_frequency)
# 定位方法封装
    @staticmethod
    def split_locator(locator):
        """
        分解定位表达式，如'css,username',拆分后返回'css selector'和定位表达式'username'(class为username的元素)
        （需要处理元素定位错误的情况）
        :param locator: 定位方法+定位表达式组合字符串，如'css,username'
        :return: locator_dict[by], value:返回定位方式和定位表达式
        """
        by = locator.split(',', 1)[0]
        value = locator.split(',', 1)[1]
        locator_dict = {
            'id': 'id',
            'name': 'name',
            'class': 'class name',
            'tag': 'tag name',
            'link': 'link text',
            'plink': 'partial link text',
            'xpath': 'xpath',
            'css': 'css selector',
        }
        if by not in locator_dict.keys():
            raise NameError("定位错误，请使用id/name/class/tag/link/plink/xpath/css方式定位，例如:'id,username'这种形式")
        return locator_dict[by], value

# 等待方式
    @staticmethod
    def sleep(sec):
        time.sleep(sec)
        log.info("设定页面等待时间 %s 秒" % sec)

    def wait_element(self, locator):
        """
        等待元素出现
        :param locator:
        """
        by, value = self.split_locator(locator)
        try:
            self.wait.until(lambda x: x.find_element(by=by, value=value), message="等待超时，该元素未找到！")
            log.info("正在等待元素：%s" % locator)
            return True
        except TimeoutException:
            return False
        except Exception as e:
            raise e

# 进程控制
    def open(self, url):
        """
        打开网址
        """
        self.driver.get(url)
        log.info('打开网址：{}'.format(url))

    def quit(self):
        """
        结束所有浏览器进程
        """
        self.driver.quit()
        log.info("关闭所有窗口，退出浏览器！")

    def close(self):
        """
        关闭当前窗口（浏览器进程不会关闭）
        """
        self.driver.close()
        log.info("关闭当前窗口！")

    def refresh(self):
        """
        刷新页面
        """
        self.driver.refresh()
        log.info("刷新当前页面")

# 页面操作方法
    def get_current_url(self):
        """
        获取当前被测网址地址
        """
        try:
            log.info("获取成功，当前url为：{}".format(self.driver.current_url))
        except Exception as e:
            log.error("获取当前url失败，错误信息为：{}".format(e))
        return self.driver.current_url

    def get_title(self):
        """
        :return: 获取网页title
        """
        log.info("获取网页title："+self.driver.title)
        return self.driver.title

    def get_placeholder(self, locator):
        """

        :param locator: 定位器
        :return: 返回placeholder属性值
        """
        elem = self.get_element(locator)
        try:
            # get_attribute获取元素标签内容
            elem_placeholder_text = elem.get_attribute("placeholder")
            log.info("该元素对象获取placeholder成功，placeholder值为：{}".format(elem_placeholder_text))
            return elem_placeholder_text
        except Exception as e:
            log.error("该元素对象获取placeholder失败，错误信息为：{}".format(e))

    def get_element(self, locator):
        """
        :param locator:没定位到抛出Timeout异常
        :return: 返回单个元素对象
        """
        if self.wait_element(locator):
            by, value = self.split_locator(locator)
            try:
                element = self.driver.find_element(by=by, value=value)
                log.info("已定位到元素：%s" % locator)
                return element

            except Exception as e:
                raise e
        else:
            return False
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency).until(
            EC.presence_of_element_located(locator)
        )

    def get_elements(self, locator):
        """
        :param locator:没定位到抛出Timeout异常
        :return: 获取所有元素列表
        """
        if not isinstance(locator, tuple):
            by, value = self.wait_element(locator)
            try:
                element = self.driver.find_element(by=by, value=value)
                log.info("已定位到元素：%s" % locator)
                return element
            except:
                raise log.info("参数类型错误，locator必须是元祖类型：loc = (id,value1)")
        else:
            return False

    def type(self, locator, value):
        """
        在元素中输入内容
        :param locator:
        :param value: 输入的内容
        """
        try:
            self.get_element(locator).send_keys(value)
            log.info("正在向元素：%s，输入文本：%s" % (locator, value))
        except Exception as e:
            log.error("元素对象输入值失败，错误信息为：{}".format(e))

    def type_all(self, locator, value):
        """
        在符合条件的所有元素中输入内容，依次循环输入value1,value2……
        :param locator:
        :param value: 输入的内容
        """
        allt = self.get_elements(locator)
        i = 1
        log.info("send_keys开始执行type_all方法，共 %s 个元素被执行" % (len(allt)))
        for ele in allt:
            newtext = value + str(i)
            ele.send_keys(newtext)
            log.info("正在向第：%s 个元素，输入文本：%s" % (i, newtext))
            i += 1

    def click(self, locator):
        """
        :param locator:
        :return:点击操作
        """
        try:
            ele = self.get_element(locator)
            ele.click()
            log.info("点击元素：" + str(locator))
        except Exception as e:
            log.error("点击元素：{} 失败，错误信息为：{}".format(locator, e))

    def clear(self, locator):
        """
        清除元素中的内容
        """
        try:
            self.get_element(locator).clear()
            log.info("清空内容：%s" % locator)
        except Exception as e:
            log.error("清除内容：{} 失败，错误信息为：{} ".format(locator, e))

    def get_text(self, locator):
        '''获取文本'''
        try:
            t = self.get_element(locator).text()
            log.info("获取text文本为：{}".format(str(t)))
            return t
        except:
            log.error("获取text文本失败，返回空字符串 ")
            return ""

    def get_attribute(self, locator, attribute):
        """
        返回元素某属性的值
        :param locator:
        :param attribute: 属性名称
        :return: 属性值
        """
        value = self.get_element(locator).get_attribute(attribute)
        log.info('获取元素 %s 的属性值 %s 为：%s' % (locator, attribute, value))
        return value

# JS操作方法

    def js(self, script):
        """
        执行JavaScript
        :param script:js语句
        """
        self.driver.execute_script(script)
        log.info("执行JS语句：%s" % script)

    def js_focus_element(self, locator):
        """
        聚焦元素（滚动条操作前置）
        """
        log.info("聚焦元素："+str(locator))
        try:
            target = self.get_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
        except Exception as e:
            log.error("聚焦元素：{} 失败，错误信息为：{}".format(locator,e))

    def js_scroll_top(self):
        """
        滚动到顶部
        """
        log.info("调用Js滚动到顶部")
        try:
            js = "window.scrollTo(0,0)"
            self.driver.execute_script(js)
            log.info("滚动成功")
        except Exception as e:
            log.error("滚动失败，错误信息为：{}".format(e))

    def js_scroll_end(self, x=0):
        """
        :param x: 默认值
        :return: 滚动到底部
        """
        log.info("调用Js滚动到底部")
        try:
            js = "window.scrollTo(%s,document.body.scrollHeight)" % x
            self.driver.execute_script(js)
            log.info("滚动成功")
        except Exception as e:
            log.error("滚动失败，错误信息为：{}".format(e))

    def js_scroll_element(self, locator):
        """
        拖动滚动条至目标元素
        """
        script = "return arguments[0].scrollIntoView();"
        element = self.get_element(locator)
        self.driver.execute_script(script, element)
        log.info("滚动至元素：%s" % locator)

# option操作方法

    def select_by_index(self, locator, index=0):
        """
        :param locator:
        :param index: 下标
        :return: 以index下标来查找该option并选择，从0开始默认选择第一个
        """
        log.info("根据【下标】查找下拉选择项：{}".format(index))
        try:
            element = self.get_element(locator)  # 定位select这一栏
            Select(element).select_by_index(index)
            log.info("成功定位到下拉select项")
        except Exception as e:
            log.error("定位select失败，错误信息为：{}".format(e))

    def select_by_value(self, locator, value):
        """
        :param locator:
        :param value:
        :return: 以value属性值来查找该option并选择
        """
        log.info("根据【属性】查找下拉选择项：{}".format(value))
        try:
            element = self.get_element(locator)
            Select(element).select_by_value(value)
            log.info("成功定位到下拉select项")
        except Exception as e:
            log.error("定位select失败，错误信息为：{}".format(e))

    def select_by_text(self, locator, text):
        """
        :param locator:
        :param text:
        :return: 以text文本属性值来查找该option并选择
        """
        log.info("根据【文本】查找下拉选择项：{}".format(text))
        try:
            element = self.get_element(locator)
            Select(element).select_by_visible_text(text)
        except Exception as e:
            log.error("定位select失败，错误信息为：{}".format(e))

    def switch_to_iframe(self, locator):
        ele = self.get_element(locator)
        try:
            self.driver.switch_to.frame(ele)
        except:
            log.exception("切换到iframe：%s 失败" % locator)
            raise

    def switch_handle(self, window_name):
        """
        :param window_name: 窗口名称
        :return: 切换handler窗口
        """
        log.info("切换handler成功！！！")
        self.driver.switch_to.window(window_name)

    def alert_accept(self):
        """
        alert点确认
        """
        self.driver.switch_to.alert.accept()
        log.info("点击弹框确认")

    def alert_dismiss(self):
        """
        alert点取消
        """
        self.driver.switch_to.alert.dismiss()
        log.info("点击弹框取消")




# 鼠标操作

    def right_click(self, locator):
        """
        鼠标右击元素
        """
        element = self.get_element(locator)
        ActionChains(self.driver).context_click(element).perform()
        log.info("在元素上右击：%s" % locator)

    def double_click(self, locator):
        """
        双击元素
        """
        element = self.get_element(locator)
        ActionChains(self.driver).double_click(element).perform()
        log.info("在元素上双击：%s" % locator)

    def move_to_element(self, locator):
        """
        :param locator:
        :return: 鼠标悬停操作
        """
        log.debug("鼠标悬停在元素："+str(locator))
        try:
            ele = self.get_element(locator)
            ActionChains(self.driver).move_to_element(ele).perform()
        except:
            log.error("悬停元素失败！")

    def drag_and_drop(self, locator, target_locator):
        """
        拖动一个元素到另一个元素位置
        :param target_locator: 目标位置元素的定位
        """
        element = self.get_element(locator)
        target_element = self.get_element(target_locator)
        ActionChains(self.driver).drag_and_drop(element, target_element).perform()
        log.info("把元素 %s 拖至元素 %s" % (locator, target_locator))

    def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
        """
        拖动一个元素移动x,y个偏移量
        :param xoffset: X offset to move to
        :param yoffset: Y offset to move to
        """
        element = self.get_element(locator)
        ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset, yoffset).perform()
        log.info("把元素 %s 拖至坐标：%s,%s" % (locator, xoffset, yoffset))

    def get_element_offset(self, locator):
        """
        获取元素坐标
        :return: x,y
        """
        element = self.get_element(locator)
        loc = element.location
        x = loc['x']
        y = loc['y']
        log.info("获取元素坐标：%s,%s" % (x, y))
        return x, y

    def get_element_offset_click(self, locator):
        """
        获取元素坐标并点击中间位置，适用于：元素A中套着元素B，元素B无法定位但元素A可以定位
        """
        element = self.get_element(locator)
        loc = element.location
        x = loc['x']
        y = loc['y']
        size = element.size
        width = size['width']
        height = size['height']
        x += width
        y += height
        self.click_offset(x, y)

    def click_offset(self, x, y):
        """
        点击坐标
        :param x: x坐标'
        :param y: y坐标'

        """
        ActionChains(self.driver).move_by_offset(x, y).click().perform()
        log.info("点击坐标%s,%s" % (x, y))

    def wait_text(self, text, per=3, count=10):
        """
        判断给定文本是否在页面上
        :param text: 要判断的文本
        :param per: 每次判断间断时间
        :param count: 判断次数
        :return: 存在返回True，不存在返回False
        """
        for i in range(count):
            if text in self.driver.page_source:
                log.info("判断页面上有文本：%s 第 %s 次" % (text, i+1))
                return True
            self.sleep(per)
        log.info("判断页面上没有文本：%s ，共 %s 次" % (text, i+1))
        return False

    def screenshot(self, info='-'):
        """
        截图,起名为：文件名-方法名-注释
        :param info: 截图说明
        """
        catalog_name = conf.get_value('screenshot_path')  # 从全局变量取截图文件夹位置
        if not os.path.exists(catalog_name):
            os.makedirs(catalog_name)

        # 截图时间
        fmt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        # 获得测试方法名称
        testcase_name = inspect.stack()[1][3]  
        # 截图存储路径   时间-方法.png
        screen_shot_name = "{0}-{1}.png".format(fmt,testcase_name)
        screen_img = catalog_name + screen_shot_name

        self.driver.get_screenshot_as_file(screen_img)
        log.info("失败截图：{0} ,失败原因：{1}".format(screen_shot_name,info))

    @staticmethod
    def create_dirs(file_dir):
        """
        创建文件路径,先判断目录是否存在
        :param file_dir:
        :return:
        """
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    def title_is(self, expect_title):
        """
        判断title是否出现，type is bool
        :param expect_title: 传入期待的title信息,type is string
        :return:bool
        """
        try:
            self.wait.until(EC.title_is(expect_title))

        except Exception as e:
            current_title = self.get_title()
            log.error('断言title未出现，当前title为：%s' % current_title)
            raise e

    def title_contains(self, expect_contain_text):
        """
        判断title是否包含某些字符
        :param expect_contain_text: 期待包含的字符，type is string
        :return:bool
        """
        try:
            self.wait.until(EC.title_contains(expect_contain_text))
        except Exception as e:
            current_title = self.get_title()
            log.error('断言title不包含：{}，当前title为：{}'.format(expect_contain_text, current_title))
            raise e


if __name__ == '__main__':
    conf.init()
    bp = BasePage()
    bp.open("www.baidu.com")
    bp.title_contains("百度")
