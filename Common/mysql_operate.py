#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/3/7 14:11
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import pymysql, logging
import run
import Common.config as conf
from Common.read_data import ReadFileData as rf
from Common.basepage import BasePage


# MySQL数据库操作
class MySQL:

    def __init__(self, db_conf):

        try:
            # 设置一个函数用来接收run传给此方法的mysql数据
            self.db_conf = rf.load_yaml(run.set_mysql()['mysql'])
            self.conn = pymysql.connect(**db_conf, autocommit=True, charset='utf-8')
            logging.info(self.conn)
        except pymysql.err.OperationalError as e:
            logging.error("Mysql客户端连接失败! %d: %s" % (e.args[0], e.args[1]))

        # 设置返回数据类型，DictCursor以字典的形式返回操作结果
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def select_db(self, sql):
        """

        :param sql: 数据库查询
        :return:
        """
        self.conn.ping(reconnect=True)
        try:
            self.cur.execute(sql)
            select_data = self.cur.fetchall()
            return select_data
        except Exception as e:
            logging.error(f'执行Mysql sql错误{e}')

    def execute_db(self, sql):
        """

        :param sql: 更新/插入/删除
        :return:
        """
        try:
            self.conn.ping(reconnect=True)
            # execute执行sql语句
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except BaseException as error:
            logging.info(f"操作MySQL出现错误，错误原因：{error}")
            # 事务回滚
            self.conn.rollback()

