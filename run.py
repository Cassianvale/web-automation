#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pytest, argparse
from Common.logger import Logger
from selenium import webdriver
import Common.config as conf


def get_args():
    """命令行参数解析"""
    parser = argparse.ArgumentParser(description='可选择参数：')
    parser.add_argument('-e', '--environment', choices=['staging', 'prepord'], default='staging', help='测试环境staging, 预生产环境prepord')
    args = parser.parse_args()

    # Staging测试环境
    if args.environment in ('test', 'staging'):
        conf.set_value('environment', 'staging')
        conf.set_value('site', 'https://account.retiehe.com/')
    # prepord预生产环境
    elif args.environment in ('pre', 'prepord'):
        conf.set_value('environment', 'prepord')
        conf.set_value('site', 'xxxxxxxx') 
    else:
        print("请输入staging或prepord！")
        exit()


def set_driver():
    """设置driver路径"""
    # 配置Chrome Driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')  # 浏览器最大化
    chrome_options.add_argument('--disable-infobars')  # 不提醒chrome正在受自动化软件控制
    prefs = {'download.default_directory': conf.get_value('download_path')}
    chrome_options.add_experimental_option('prefs', prefs)  # 设置默认下载路径
    # chrome_options.add_argument(r'--user-data-dir=D:\ChromeUserData')  # 设置用户文件夹，可免登陆
    driver = webdriver.Chrome('{}/Driver/chromedriver'.format(conf.get_value('root_path')), options=chrome_options)
    conf.set_value('driver', driver)


def set_mysql(value='staging'):
    if value == 'staging':
        test_staging = "{}/Setting/test_staging.yaml".format(conf.get_value('root_path'))
        conf.set_value('staging_path', test_staging)
    elif value == 'test_preprod':
        test_preprod = "{}/Setting/test_preprod.yaml".format(conf.get_value('root_path'))
        conf.set_value('preprod_path', test_preprod)


def main():
    """运行pytest命令启动测试"""
    "需要定义测试用例集合"
    pytest.main(['-v', '-s', './TestCases/staging_cases', '--html=File/report/report.html', '--self-contained-html'])


if __name__ == "__main__":
    conf.init()  # 初始化全局变量
    get_args()  # 命令行参数解析设置全局变量
    log = Logger('test')  # 初始化log配置
    set_driver()  # 初始化driver
    main()  # 运行pytest测试集
    conf.get_value('driver').quit()  # 关闭selenium driver

    # 发送邮件前提先将Common.mail文件send_mail()中的用户名、密码填写正确
    # send_mail(['1430066373@qq.com'])  # 将报告发送至邮箱
