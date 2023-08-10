#!/usr/bin/python3  
# -*- coding: utf-8 -*-

"""
@Project      : sqlalchemy_test

@Email        : 562140134@qq.com

@Modify Time  : 2023-08-09 9:26

@Author       : Arthas

@Version      : 1.0

@IDE          : PyCharm


===============

@Description  :

===============
"""
import abc
from typing import Generic, TypeVar, Dict, Union, List, Tuple, Type

from demo.model_demo.base_model import BaseModel, FieldSortEnum, Fields
from demo.model_demo.models import TestModel
from demo.model_demo.sql_utils import BuildSQLException

T = TypeVar('T')


class AbstractSQL(Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build(self) -> str:
        """
        构建SQL的函数, 调用后返回可执行SQL
        Returns:

        """
        pass

    @abc.abstractmethod
    def re_set(self):
        """
        重置已经构建的sql
        Returns:

        """
        pass

    # noinspection PyUnresolvedReferences
    def replace_placeholder(self, use_placeholder: str):
        return self.sql.replace('?', use_placeholder)


class AbstractWhere(AbstractSQL):

    @abc.abstractmethod
    def where(self, *conditions):
        """
        构建where条件sql函数
        例如:
            WhereImpl().where(TestModel.id==1, TestModel.name=='张三')
        Args:
            *conditions (): 条件元组({'id': 1}, {'name': 2})

        Returns:
            WHERE id=1 AND name='张三'
        """
        pass

    # noinspection PyMethodMayBeStatic
    def condition_processor(self, *conditions) -> Dict:
        """
        把条件列表解包为字典例如

            >>>[{'id': 1}, {'name': '张三'}] #

        Args:
            *conditions (): 条件列表

        Returns:
            {'id': 1, 'name': '张三'}
        """
        result = {}
        for c in conditions:
            result.update(c)
        return result

    # noinspection PyMethodMayBeStatic
    def condition_dict_processor(self, condition_dict: Dict) -> Tuple[List[str], List]:
        """
        将条件字典转换为sql中的key=value的形式

        Args:
            condition_dict ():

        Returns:

        """
        condition_str_list = []
        sql_params = []
        for k, v in condition_dict.items():
            sql_params.append(v)
            if '%' not in v:
                condition_str_list.append(f'{k}=?')
            else:
                condition_str_list.append(f'{k} LIKE ?')
        return condition_str_list, sql_params


class AbstractInsert(AbstractSQL):

    @abc.abstractmethod
    def insert(self, model: BaseModel = None):
        pass


class AbstractDelete(AbstractSQL):

    @abc.abstractmethod
    def delete(self, params: Dict, table_name: str = ''):
        pass


class AbstractUpdate(AbstractSQL):

    @abc.abstractmethod
    def update(self, params: Dict, table_name: str = ''):
        pass


class AbstractSelect(AbstractSQL):

    @abc.abstractmethod
    def select(self, model: Type[BaseModel] = None, fields: List[Fields] = None):
        pass

    @abc.abstractmethod
    def order_by(self, *fields_sort: Tuple[FieldSortEnum]) -> str:
        """
        根据传入的字段拼接排序sql
        例如
            SelectImpl().select().order_by(fields_sort=[Test.id.desc])
        Args:
            fields_sort (): 排序字段的FieldSortEnum枚举类型

        Returns:
        order by sql
        """

        pass

    @abc.abstractmethod
    def group_by(self, fields=()) -> str:
        """
        根据传入字段拼接分组sql
        例如
            SelectImpl().select().group_by(fields_sort=[Test.name])
        Args:
            fields (): 分组字段列表

        Returns:
        order by sql
        """
        pass


class AbstractJoin(AbstractSQL):

    @abc.abstractmethod
    def join(self, table: Union[str, BaseModel], on):
        pass


class WhereImpl(AbstractWhere):

    def __init__(self):
        self.__sql = ''
        self.__sql_params = []

    @property
    def sql(self):
        return self.__sql

    @property
    def sql_params(self):
        return self.__sql_params

    def where(self, *conditions):
        condition_dict = self.condition_processor(*conditions)

        where_condition, sql_params = self.condition_dict_processor(condition_dict)

        self.__sql_params = sql_params

        result = ' AND '.join(where_condition)

        self.__sql = ' WHERE {where_condition}'

        if conditions:
            self.__sql = self.__sql.format(where_condition=result)

        return self

    def build(self) -> str:
        return self.__sql

    def re_set(self):
        self.__sql = ''
        self.__sql_params = []
        return self


class SelectImpl(AbstractSelect):

    # noinspection SqlNoDataSourceInspection
    def __init__(self, fields: List = None, model: Type[BaseModel] = None):
        self.__fields = fields
        self.__table_name = model.__table_name__ if model else None
        self.__sql = 'SELECT {fields} FROM {table_name}'
        self.__group_by = ''
        self.__order_by = ''

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

    @property
    def sql(self):
        return self.__sql

    def select(self, model: Type[BaseModel] = None, fields: List[Fields] = None):
        select_params = {}

        if model:
            self.table_name = model.__table_name__
            select_params['table_name'] = self.table_name
        else:
            select_params['table_name'] = self.table_name

        if fields:
            self.fields = list(map(lambda f: self.table_name + '.' + f.db_column_name, fields))
            select_params['fields'] = ', '.join(self.fields)
        else:
            select_params['fields'] = '*'

        self.__sql = self.__sql.format(**select_params)

        return self

    def order_by(self, *fields_sort: Tuple[str]) -> str:
        sql = ' ORDER BY {order_by}'
        if fields_sort:
            sort_list = list(map(lambda f: self.table_name + '.' + f, fields_sort))
            order_by_fields_sql = ', '.join(sort_list)
            self.__order_by = sql.format(order_by=order_by_fields_sql)
        else:
            self.__order_by = sql.format(order_by='id desc')
        return self.__order_by

    def group_by(self, *fields: Tuple[Fields]) -> str:
        if fields:
            sql = ' GROUP BY {group_sql}'
            group_by_fields_sql = ', '.join(list(map(lambda f: self.table_name + '.' + f.db_column_name, fields)))
            self.__group_by = sql.format(group_sql=group_by_fields_sql)
        else:
            self.__group_by = ''
        return self.__group_by

    def build(self) -> str:
        if self.__order_by:
            self.__sql += self.__order_by

        if self.__group_by:
            self.__sql += self.__group_by

        return self.__sql

    # noinspection SqlNoDataSourceInspection
    def re_set(self, fields: List = (), table_name: str = ''):
        self.__fields = fields
        self.__table_name = table_name
        self.__sql = 'SELECT {fields} FROM {table_name}'
        self.__group_by = ''
        self.__order_by = ''


class InsertImpl(AbstractInsert):

    # noinspection SqlNoDataSourceInspection
    def __init__(self, model: BaseModel = None):
        self.__sql = 'INSERT INTO {table_name} ({fields}) VALUE ({values})'
        self.__table_name = model.__table_name__ if model else ''
        if model:
            params = self.__iter_model(model)
            self.__fields = list(map(str, params.keys()))
            self.__sql_params = list(map(str, params.values()))

    @property
    def sql(self):
        return self.__sql

    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, table_name: str):
        self.__table_name = table_name

    @property
    def sql_params(self):
        return self.__sql_params

    def insert(self, model: BaseModel = None):
        insert_params = {}
        if model:
            self.table_name = model.__table_name__
            insert_params['table_name'] = self.table_name
            params = self.__iter_model(model=model)
        elif self.table_name:
            insert_params['table_name'] = self.table_name
            params = self.__sql_params
        else:
            raise BuildSQLException('为找到insert数据需要的表名称')

        if params:
            fields = list(map(str, params.keys()))
            insert_params['fields'] = ', '.join(fields)
            self.__sql_params = list(map(str, params.values()))
            values = ['?'] * len(self.__sql_params)
            insert_params['values'] = ', '.join(values)
        elif self.__sql_params:
            insert_params['fields'] = ', '.join(self.__fields)
            values = ['?'] * len(self.__sql_params)
            insert_params['values'] = ', '.join(values)
        else:
            raise BuildSQLException('为找到insert数据需要的values')

        self.__sql = self.__sql.format(**insert_params)

        return self

    def build(self) -> str:
        return self.__sql

    # noinspection SqlNoDataSourceInspection
    def re_set(self):
        self.__sql = 'INSERT INTO {table_name} ({fields}) VALUE ({values})'
        self.__table_name = ''
        self.__fields = None
        self.__sql_params = None

    # noinspection PyMethodMayBeStatic
    def __iter_model(self, model: BaseModel):
        params = {}
        for k, v in model.__dict__.items():
            if k.startswith('__') or k.endswith('__'):
                continue
            params[k] = v
        return params


if __name__ == '__main__':
    def test_select():
        s = SelectImpl()
        sql = s.select(model=TestModel, fields=[TestModel.id]).build()
        print('select ---', sql)
        order_by = s.order_by(TestModel.name.desc, TestModel.id.asc)
        print('order_by ---', order_by)
        group_by = s.group_by(TestModel.name, TestModel.id)
        print('group_by ---', group_by)
        print('select ---', s.build())


    def test_where():
        w = WhereImpl()
        w_sql = w.where(TestModel.name.like('%三%')).build()
        print(w_sql, 'like-------', w.sql_params)
        w_sql1 = w.where(TestModel.name == '张三').build()
        print(w_sql1, '-------', w.sql_params)


    def test_insert():
        t = TestModel(id=1, name='张三')
        i = InsertImpl()
        sql = i.insert(t).build()
        print('sql ----', sql)
        print('params ----', i.sql_params)
        print(i.replace_placeholder('%s'))


    test_select()
    test_where()
    test_insert()
