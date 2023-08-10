#!/usr/bin/python3  
# -*- coding: utf-8 -*-

"""
@Project      : sqlalchemy_test

@Email        : 562140134@qq.com

@Modify Time  : 2023-08-08 13:23

@Author       : Arthas

@Version      : 1.0

@IDE          : PyCharm


===============

@Description  :

===============
"""
from demo.model_demo.base_model import BaseModel, INTEGER, STRING


class TestModel(BaseModel):
    # __table_name__ = 'test'

    id = INTEGER('id')
    name = STRING('name', 32)


if __name__ == '__main__':
    t = TestModel()
    t.id=1
    t.name='张三'
    sql = t.query.select().where(TestModel.id == 1, TestModel.name == '张三')
    a = iter(sql)
    for i in a:
        print(i)
