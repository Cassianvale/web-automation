#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/5/19 21:39
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import xlrd


class ExcelOption:
    @staticmethod
    def read_excel(file_name, index):
        """
        file_name: 文件名
        index: 索引
        Return:字典
        """
        test_data_path = file_name
        xls = xlrd.open_workbook(test_data_path)
        sheet = xls.sheet_by_index(index)
        data_dir = {}
        for i in range(sheet.ncols):
            data = []
            for j in range(sheet.nrows):
                if j == 0:
                    continue
                else:
                    data.append(sheet.row_values(j)[i])
            data_dir[i] = data
        return data_dir
