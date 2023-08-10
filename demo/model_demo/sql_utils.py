#!/usr/bin/python3  
# -*- coding: utf-8 -*-

"""
@Project      : sqlalchemy_test

@Email        : 562140134@qq.com

@Modify Time  : 2023-08-08 14:05

@Author       : Arthas

@Version      : 1.0

@IDE          : PyCharm


===============

@Description  :

===============
"""
import enum
from typing import List, Dict


class BuildSQLFlagEnum(enum.Enum):
    unknown = 0
    insert = 1
    delete = 2
    update = 3
    select = 4


class BuildSQLException(Exception):
    pass


class BuildSQLUtil:

    def __init__(self, fields: List = (), table_name: str = ''):
        self.__index = 0
        self.__fields = fields
        self.__table_name = table_name
        self.__select = 'SELECT {fields} FROM {table_name}'
        self.__where = ''
        self.__update = 'UPDATE {table_name} SET'
        self.__insert = 'INSERT INTO {table_name} ({fields}) VALUE ({values})'
        self.__delete = 'DELETE FROM {table_name}'
        self.__build_flag = BuildSQLFlagEnum.unknown

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields: List):
        self.__fields = fields

    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, table_name: str):
        self.__table_name = table_name

    def insert(self, params: Dict, table_name: str = ''):
        insert_params = {}
        if table_name:
            self.table_name = table_name
            insert_params['table_name'] = self.table_name
        else:
            insert_params['table_name'] = self.table_name

        if params:
            fields = list(map(str, params.keys()))
            values = list(map(str, params.values()))
            insert_params['fields'] = ','.join(fields)
            insert_params['values'] = ','.join(values)
        else:
            raise BuildSQLException('insert 必须传入params字典')

        self.__verify_type(BuildSQLFlagEnum.insert)

        self.__insert = self.__insert.format(**insert_params)

        return self

    def select(self, fields=(), table_name=''):
        select_params = {}
        if fields:
            self.fields = fields
            select_params['fields'] = ','.join(fields)
        else:
            select_params['fields'] = '*'

        if table_name:
            self.table_name = table_name
            select_params['table_name'] = table_name
        else:
            select_params['table_name'] = self.table_name

        self.__verify_type(BuildSQLFlagEnum.select)

        self.__select = self.__select.format(**select_params)
        return self

    def where(self, *conditions):
        condition_dict = self.__condition_processor(*conditions)
        where_condition = self.__condition_dict_processor(condition_dict)
        where_sql = ' WHERE {where_condition}'
        result = ' AND '.join(where_condition)
        if conditions:
            self.__where = where_sql.format(where_condition=result)
        return self

    def build(self):
        # 增
        if self.__build_flag.value == 1:
            result = self.__insert
        # 删
        elif self.__build_flag.value == 2:
            result = self.__delete + self.__where
        # 改
        elif self.__build_flag.value == 3:
            result = self.__update + self.__where
        # 查
        elif self.__build_flag.value == 4:
            result = self.__select + self.__where
        else:
            raise BuildSQLException('未知的sql构建类型')
        self.__build_flag = BuildSQLFlagEnum.unknown
        return result

    def __verify_type(self, build_flag: BuildSQLFlagEnum):
        if self.__build_flag.value:
            raise BuildSQLException(
                '不能将{old_build_flag}更改为{now_build_flag}'.format(old_build_flag=self.__build_flag.name,
                                                                      now_build_flag=build_flag.name))
        self.__build_flag = build_flag

    def __condition_processor(self, *conditions) -> Dict:
        result = {}
        for c in conditions:
            result.update(c)
        return result

    def __condition_dict_processor(self, condition_dict:Dict) -> List[str]:
        condition_str_list = []
        for k, v in condition_dict.items():
            condition_str_list.append(f'{k}={v}')
        return condition_str_list

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self.data))
            return [self.data[i] for i in range(start, stop, step)]
        else:
            return self.data[item]

    def __iter__(self):
        return self

    def __next__(self):
        return self.build()

if __name__ == '__main__':
    u = BuildSQLUtil(table_name='test')
    sql = u.select().where().build()
    print(sql)

    u1 = BuildSQLUtil(table_name='test')
    sql = u.insert(params={'id':1, 'name': '张三'}).build()
    print(sql)
