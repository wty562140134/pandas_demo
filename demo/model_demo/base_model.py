#!/usr/bin/python3  
# -*- coding: utf-8 -*-

"""
@Project      : sqlalchemy_test

@Email        : 562140134@qq.com

@Modify Time  : 2023-08-08 10:05

@Author       : Arthas

@Version      : 1.0

@IDE          : PyCharm


===============

@Description  : 手撸模型基础类

===============
"""
import enum
from typing import Union, Dict, Tuple, List

from demo.model_demo.sql_utils import BuildSQLUtil


class FieldSortEnum(enum.Enum):
    """
    排序枚举
    """
    asc = 'ASC'
    desc = 'DESC'


class ConditionDict(dict):

    def __init__(self, sql: str = '', sql_params: List = '', seq=None, **kwargs):
        kwargs['sql'] = sql
        kwargs['sql_params'] = sql_params
        super(ConditionDict, self).__init__(seq=seq, **kwargs)

    def __eq__(self, other: Dict):
        """
        重写等于比较函数用于在比较两个ConditionDict对象的值即做==操作

        Args:
            other ():

        Returns:

        """
        print(other)

    def __ne__(self, other):
        """
        重写不等于比较函数用于在比较两个ConditionDict对象的值即做!=操作

        Args:
            other ():

        Returns:

        """

        print(other)

    def __and__(self, other):
        """
        重写与函数用于在比较两个ConditionDict对象的值即做&操作

        Args:
            other ():

        Returns:

        """
        print(other)

    def __or__(self, other):
        """
        重写或比较函数用于在比较两个ConditionDict对象的值即做|操作

        Args:
            other ():

        Returns:

        """
        print(other)
        other.update(self)
        sql = ''
        sql_params = []
        for k, v in other.items():
            if 'in_' in k:
                params_len = len(v)
                placeholder = ', '.join(params_len * ['?'])
                sql = k.split('in_')[-1] + ' in (' + placeholder + ')'
                if isinstance(v, List):
                    sql_params += v
                else:
                    sql_params.append(v)

            if 'like' in k:
                if sql:
                    sql += ' and ' + k.split('like_')[-1] + ' like ?'
                else:
                    sql = k.split('like')[-1] + ' like ?'
                sql_params.append(v)

        return ConditionDict(sql=sql, sql_params=sql_params)
        # return sql, sql_params

    def __gt__(self, other):
        """
        重写大于比较函数用于在比较两个ConditionDict对象的值即做>操作

        Args:
            other ():

        Returns:

        """
        print(other)

    def __ge__(self, other):
        """
        重写大于等于比较函数用于在比较两个ConditionDict对象的值即做>=操作

        Args:
            other ():

        Returns:

        """

        print(other)

    def __lt__(self, other):
        """
        重写小于比较函数用于在比较两个ConditionDict对象的值即做<操作

        Args:
            other ():

        Returns:

        """

    def __le__(self, other):
        """
        重写小于等于比较函数用于在比较两个ConditionDict对象的值即做<=操作

        Args:
            other ():

        Returns:

        """


class Fields:

    def __init__(self, db_column_name: str, db_column_len: Union[str, int] = ''):
        self.__db_column_name = db_column_name
        if self.__class__.__name__ == 'STRING':
            self.__db_column_len = f'VARCHAR({db_column_len})'
        else:
            self.__db_column_len = f'{self.__class__.__name__}{db_column_len}'
        self.__conditions_dict = {}
        self.__sort = None

    @property
    def db_column_name(self):
        return self.__db_column_name

    @db_column_name.setter
    def db_column_name(self, db_column_name: Union[str, int]):
        self.__db_column_name = db_column_name

    @property
    def db_column_len(self):
        return self.__db_column_len

    @db_column_len.setter
    def db_column_len(self, db_column_len):
        self.__db_column_len = db_column_len

    @property
    def asc(self) -> str:
        """
        正序

        Returns:

        """
        self.__sort = FieldSortEnum.asc
        return self.db_column_name + ' ' + self.__sort.value

    @property
    def desc(self) -> str:
        """
        倒序

        Returns:

        """
        self.__sort = FieldSortEnum.desc
        return self.db_column_name + ' ' + self.__sort.value

    def like(self, like_condition):
        conditions_dict = ConditionDict()
        conditions_dict['like_' + self.__db_column_name] = like_condition
        return conditions_dict

    def in_(self, in_condition: Union[List]):
        conditions_dict = ConditionDict()
        if isinstance(in_condition, List):
            conditions_dict['in_' + self.__db_column_name] = in_condition
        return conditions_dict

    def __eq__(self, other):
        conditions_dict = ConditionDict()
        conditions_dict[self.db_column_name] = other
        return conditions_dict


class STRING(Fields):
    pass


class INTEGER(Fields):
    pass


class ModelMetaClass(type):

    def __init__(cls, name: str, bases: Tuple, namespace: Dict):
        if name != 'BaseModel':
            mappings = {}
            for attr_name, attr_value in namespace.items():
                if isinstance(attr_value, Fields) and (not attr_name.startswith('__') and not attr_name.endswith('__')):
                    mappings[attr_name] = attr_value
            cls.__mappings__ = mappings
            if mappings.get('__table_name__'):
                table_name = mappings.get('__table_name__')
            else:
                table_name = name.split('Model')[0].lower()
            cls.__table_name__ = table_name
            cls.query = BuildSQLUtil(table_name=table_name)
        super(ModelMetaClass, cls).__init__(name, bases, namespace)


class BaseModel(metaclass=ModelMetaClass):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        attrs = []
        for attr_name, attr_value in self.__dict__.items():
            attrs.append('{attr_name}:{attr_value}'.format(attr_name=attr_name, attr_value=attr_value))
        result = 'model_object: {model_object}<{attrs}>'.format(model_object=self.__table_name__,
                                                                attrs=', '.join(attrs))
        return result

    __repr__ = __str__
