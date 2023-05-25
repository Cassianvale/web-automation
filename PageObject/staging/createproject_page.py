#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2023/03/22 17:08
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import Common.config as conf
import logging
from Common.basepage import BasePage


class CreateProject(BasePage):

    def __init__(self, driver):
        
        self.driver = driver
        super().__init__()

    # i=输入框,b=按钮,l=链接,a=Alert弹窗,im=图片,t=文字控件,d=div,lab=label
    
    # """选择一个进行中的项目"""
    # b_project_management = "a[href = '/projects']"
    # b_active_project = "[title='pre-0613']"
    # """创建一个新的项目"""
    # b_new_project = "//*[text()='新建项目']"
    # i_project = "#title"    # 项目名称填写
    # i_select_time = "#start_at"  # 时间选择
    # photographer_id_list = "//*[@id='photographer_id']"     # 拍摄计划负责人
    # public_material_1 = "//*[@id='is_public']/label[1]/span[1]/input"  # 公开制作池素材待选 是
    # public_material_0 = "//*[@id='is_public']/label[2]/span[1]/input"  # 公开制作池素材待选 否
    # secrecy_1 = "//*[@id='is_confidential']/label[1]/span[1]/input"     # 保密 是
    # secrecy_0 = "//*[@id='is_confidential']/label[2]/span[1]/input"     # 保密 否
    # submit = "//*[text()='创 建']"
    # cancel = "//*[text()='取 消']"





