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
import enum
from typing import Generic, TypeVar, Dict, List, Tuple, Type

from demo.model_demo.base_model import BaseModel, FieldSortEnum, Fields
from demo.model_demo.models import TestModel

T = TypeVar('T')


class SQLAttributeSqlGetMixin:

    def __init__(self, sql: str):
        self.__sql = sql

    @property
    def sql(self):
        return self.__sql


class SQLAttributeSqlGetSetMixin:

    def __init__(self, sql: str):
        self.__sql = sql

    @property
    def sql(self):
        return self.__sql

    @sql.setter
    def sql(self, sql: str):
        self.__sql = sql


class SQLAttributeFieldsGetMixin:

    def __init__(self, fields: List):
        self.__fields = fields

    @property
    def fields(self):
        return self.__fields


class SQLAttributeFieldsGetSetMixin:

    def __init__(self, fields: List):
        self.__fields = fields

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields: List):
        self.__fields = fields


class SQLAttributeTableNameGetMixin:

    def __init__(self, table_name: str):
        self.__table_name = table_name

    @property
    def table_name(self):
        return self.__table_name


class SQLAttributeTableNameGetSetMixin:

    def __init__(self, table_name: str):
        self.__table_name = table_name

    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, table_name: str):
        self.__table_name = table_name


class SQLAttributeSqlParamsGetMixin:

    def __init__(self, sql_params: List):
        self.__sql_params = sql_params

    @property
    def sql_params(self):
        return self.__sql_params


class SQLAttributeSqlParamsGetSetMixin:

    def __init__(self, sql_params: List):
        self.__sql_params = sql_params

    @property
    def sql_params(self):
        return self.__sql_params

    @sql_params.setter
    def sql_params(self, sql_params: List):
        self.__sql_params = sql_params


class Condition:

    def __init__(self, conditions: Tuple):
        self.__conditions = conditions

    def get_condition(self):
        pass


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

    # noinspection PyMethodMayBeStatic
    def iter_model(self, model: BaseModel):
        params = {}
        for k, v in model.__dict__.items():
            if k.startswith('__') or k.endswith('__'):
                continue
            params[k] = v
        return params

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
            if isinstance(c, Dict):
                result.update(c)
        return result

    # noinspection PyMethodMayBeStatic,PyUnresolvedReferences
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
            if getattr(self, 'table_name', None):
                append_value = self.table_name + '.' + v.db_column_name if isinstance(v, Fields) else v
            else:
                append_value = v.db_column_name if isinstance(v, Fields) else v

            if isinstance(v, List):
                sql_params += v
            else:
                sql_params.append(append_value)

            if (isinstance(v, str) and '%' not in v) or isinstance(v, Fields):
                if getattr(self, 'table_name', None):
                    condition_str_list.append(f'{self.table_name}.{k}=?')
                else:
                    condition_str_list.append(f'{k}=?')
            elif isinstance(v, List):
                in_sql = '({})'.format(', '.join(['?'] * len(v)))
                if getattr(self, 'table_name', None):
                    condition_str_list.append(f'{self.table_name}.{k} IN {in_sql}')
                else:
                    condition_str_list.append(f'{k} IN {in_sql}')
            else:
                if getattr(self, 'table_name', None):
                    condition_str_list.append(f'{self.table_name}.{k} LIKE ?')
                else:
                    condition_str_list.append(f'{k} LIKE ?')
        return condition_str_list, sql_params


class AbstractWhere(AbstractSQL, SQLAttributeSqlGetMixin,
                    SQLAttributeSqlParamsGetMixin, SQLAttributeTableNameGetSetMixin):

    def __init__(self, sql: str, sql_params: List, table_name: str):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeSqlParamsGetMixin.__init__(self, sql_params=sql_params)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)

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


class AbstractInsert(AbstractSQL, SQLAttributeSqlGetMixin, SQLAttributeFieldsGetSetMixin,
                     SQLAttributeTableNameGetSetMixin, SQLAttributeSqlParamsGetMixin):

    def __init__(self, sql: str, table_name: str, sql_params: List, fields: List):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)
        SQLAttributeSqlParamsGetMixin.__init__(self, sql_params=sql_params)
        SQLAttributeFieldsGetSetMixin.__init__(self, fields=fields)

    @abc.abstractmethod
    def insert(self, model: BaseModel = None):
        pass


class AbstractDelete(AbstractSQL, SQLAttributeSqlGetMixin, SQLAttributeTableNameGetSetMixin):

    def __init__(self, sql: str, table_name: str):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)

    @abc.abstractmethod
    def delete(self, model: BaseModel):
        pass


class AbstractUpdate(AbstractSQL, SQLAttributeSqlGetMixin, SQLAttributeTableNameGetSetMixin,
                     SQLAttributeSqlParamsGetMixin, SQLAttributeFieldsGetSetMixin):

    def __init__(self, sql: str, table_name: str, sql_params: List, fields: List):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)
        SQLAttributeSqlParamsGetMixin.__init__(self, sql_params=sql_params)
        SQLAttributeFieldsGetSetMixin.__init__(self, fields=fields)

    @abc.abstractmethod
    def update(self, model: BaseModel = None):
        pass


class AbstractSelect(AbstractSQL, SQLAttributeSqlGetMixin,
                     SQLAttributeTableNameGetSetMixin, SQLAttributeFieldsGetSetMixin):

    def __init__(self, sql: str, fields: List, table_name):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)
        SQLAttributeFieldsGetSetMixin.__init__(self, fields=fields)

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


class AbstractJoin(AbstractSQL, SQLAttributeSqlGetMixin, SQLAttributeTableNameGetSetMixin,
                   SQLAttributeSqlParamsGetMixin):
    class JoinTypeEnum(enum.Enum):
        join = 'JOIN'
        left_join = 'LEFT JOIN'
        right_join = 'RIGHT JOIN'

    def __init__(self, sql: str, table_name: str, sql_params: List):
        SQLAttributeSqlGetMixin.__init__(self, sql=sql)
        SQLAttributeTableNameGetSetMixin.__init__(self, table_name=table_name)
        SQLAttributeSqlParamsGetMixin.__init__(self, sql_params=sql_params)

    @abc.abstractmethod
    def join(self, model: Type[BaseModel] = None, join_type: JoinTypeEnum = None):
        pass

    @abc.abstractmethod
    def on(self, *on_conditions):
        pass


class WhereImpl(AbstractWhere):

    def __init__(self, model: Type[BaseModel] = None):
        self.__sql = ''
        self.__sql_params = []
        self.__table_name = model.__table_name__ if model else ''
        super().__init__(sql=self.__sql, sql_params=self.__sql_params, table_name=self.__table_name)

    def where(self, *conditions):
        condition_dict = self.condition_processor(*conditions)

        where_condition, sql_params = self.condition_dict_processor(condition_dict)
        c = Condition(conditions=conditions)

        self.__sql_params = sql_params

        result = ' AND '.join(where_condition)

        self.__sql = ' WHERE {where_condition}'

        if conditions:
            self.__sql = self.__sql.format(where_condition=result)

        super().__init__(sql=self.__sql, sql_params=self.__sql_params, table_name=self.__table_name)

        return self

    def __eq__(self, other):
        print(other)

    def build(self) -> str:
        return self.__sql

    def re_set(self):
        self.__sql = ''
        self.__sql_params = []
        self.__table_name = ''
        super().__init__(sql=self.__sql, sql_params=self.__sql_params, table_name=self.__table_name)
        return self


class SelectImpl(AbstractSelect):

    # noinspection SqlNoDataSourceInspection
    def __init__(self, model: Type[BaseModel], fields: List = None):
        self.__model = model
        self.__fields = [i.db_column_name for i in fields] if fields else []
        self.__table_name = model.__table_name__ if model else None
        self.__sql = 'SELECT {fields} FROM {table_name}'

        if fields:
            self.__sql = self.__sql.format(fields=', '.join(self.__fields), table_name=self.__table_name)
        else:
            self.__sql = self.__sql.format(fields='*', table_name=self.__table_name)

        self.__group_by = ''
        self.__order_by = ''
        super().__init__(sql=self.__sql, table_name=self.__table_name, fields=self.__fields)

    def select(self, model: Type[BaseModel] = None, fields: List[Fields] = None):
        if model and fields:
            self.__init__(model=model, fields=fields)

        if not model and fields:
            self.__init__(model=self.__model, fields=fields)

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
    def re_set(self):
        self.__fields = []
        self.__table_name = ''
        self.__sql = 'SELECT {fields} FROM {table_name}'
        self.__group_by = ''
        self.__order_by = ''
        super().__init__(sql=self.__sql, table_name=self.__table_name, fields=self.__fields)
        return self


class InsertImpl(AbstractInsert):

    # noinspection SqlNoDataSourceInspection
    def __init__(self, model: BaseModel):
        self.__model = model
        self.__sql = 'INSERT INTO {table_name} ({fields}) VALUE ({values})'
        self.__table_name = model.__table_name__ if model else ''
        params = self.iter_model(model)
        self.__fields = list(map(str, params.keys()))
        self.__sql_params = list(map(str, params.values()))
        values = ['?'] * len(self.__sql_params)
        self.__sql = self.__sql.format(table_name=self.__table_name, fields=', '.join(self.__fields),
                                       values=', '.join(values))
        super().__init__(sql=self.__sql, table_name=self.__table_name,
                         sql_params=self.__sql_params, fields=self.__fields)

    def insert(self, model: BaseModel = None):
        if model:
            self.__init__(model=model)

        return self

    def build(self) -> str:
        return self.__sql

    # noinspection SqlNoDataSourceInspection
    def re_set(self):
        self.__sql = 'INSERT INTO {table_name} ({fields}) VALUE ({values})'
        self.__table_name = ''
        self.__fields = []
        self.__sql_params = []
        super().__init__(sql=self.__sql, table_name=self.__table_name,
                         sql_params=self.__sql_params, fields=self.__fields)
        return self


class DeleteImpl(AbstractDelete):

    def __init__(self, model):
        self.__model = model
        self.__sql = 'DELETE FROM {table_name}'
        self.__sql = self.__sql.format(table_name=model.__table_name__)
        self.__table_name = model.__table_name__
        super().__init__(sql=self.__sql, table_name=self.__table_name)

    def delete(self, model: Type[BaseModel] = None):
        if model:
            self.__init__(model=model)

        return self

    def build(self) -> str:
        return self.__sql

    def re_set(self):
        self.__sql = 'DELETE FROM {table_name}'
        self.__table_name = ''
        super().__init__(sql=self.__sql, table_name=self.__table_name)
        return self


class UpdateImpl(AbstractUpdate):

    def __init__(self, model: BaseModel):
        self.__model = model
        self.__sql = 'UPDATE {table_name} SET '
        self.__table_name = model.__table_name__
        params = self.iter_model(model)
        self.__fields = list(map(str, params.keys()))
        self.__sql_params = list(map(str, params.values()))
        self.__sql = self.__sql.format(table_name=self.__table_name)
        sql = ', '.join([f'{k}=?' for k, v in zip(self.__fields, self.__sql_params)])
        self.__sql += sql
        super().__init__(sql=self.__sql, table_name=self.__table_name,
                         sql_params=self.__sql_params, fields=self.__fields)

    def update(self, model: BaseModel = None):
        if model:
            self.__init__(model=model)
        return self

    def build(self) -> str:
        return self.__sql

    def re_set(self):
        self.__sql = 'UPDATE {table_name} SET '
        self.__table_name = ''
        self.__fields = []
        self.__sql_params = []
        super().__init__(sql=self.__sql, table_name=self.__table_name,
                         sql_params=self.__sql_params, fields=self.__fields)


class JoinImpl(AbstractJoin):
    JoinTypeEnum = AbstractJoin.JoinTypeEnum

    def __init__(self, model: Type[BaseModel], join_type: JoinTypeEnum):
        self.__model = model
        self.__sql = '{join_sql} {table_name} ON {on_condition}'
        self.__table_name = model.__table_name__
        self.__sql_params = []
        self.__sql = self.__sql.format(join_sql=join_type.value,
                                       table_name=self.__table_name,
                                       on_condition='{on_condition}')
        super().__init__(sql=self.__sql, table_name=self.__table_name, sql_params=self.__sql_params)

    def join(self, model: Type[BaseModel] = None, join_type: JoinTypeEnum = None):
        if model:
            self.__init__(model=model, join_type=join_type)
        return self

    def on(self, *on_conditions):
        condition_dict = self.condition_processor(*on_conditions)
        condition_str_list, sql_params = self.condition_dict_processor(condition_dict=condition_dict)
        self.__sql_params = sql_params
        self.__sql = self.__sql.format(on_condition=', '.join(condition_str_list))
        super().__init__(sql=self.__sql, table_name=self.__table_name, sql_params=self.__sql_params)
        return self

    def build(self) -> str:
        return self.__sql

    def re_set(self):
        self.__model = None
        self.__sql = '{join_sql} {table_name} ON {on_condition}'
        self.__table_name = ''
        self.__sql_params = []
        super().__init__(sql=self.__sql, table_name=self.__table_name, sql_params=self.__sql_params)


if __name__ == '__main__':
    def test_select():
        s = SelectImpl(model=TestModel)
        sql = s.select(fields=[TestModel.id]).build()
        print('select ---', sql)
        order_by = s.order_by(TestModel.name.desc, TestModel.id.asc)
        print('order_by ---', order_by)
        group_by = s.group_by(TestModel.name, TestModel.id)
        print('group_by ---', group_by)
        print('select ---', s.build())


    def test_where():
        w = WhereImpl(TestModel)
        print('---------like----------')
        w_sql = w.where(
            (TestModel.name.like('%三%') | TestModel.name.in_(['a', 'b'])) & TestModel.name == '张三').build()
        print('sql:', w_sql)
        print('sql_params:', w.sql_params)
        print('---------like over----------')
        print('---------==--------------')
        w_sql1 = w.where(TestModel.name == '张三').build()
        print('sql:', w_sql1)
        print('sql_params:', w.sql_params)
        print('---------== over--------------')
        print('---------in----------')
        w_sql_in = w.where(TestModel.id.in_([1, 2, 3]), TestModel.name == '张三').build()
        print('sql:', w_sql_in)
        print('sql_params:', w.sql_params)
        print('---------in over----------')


    def test_insert():
        t = TestModel(id=1, name='张三')
        i = InsertImpl(model=t)
        sql = i.insert().build()
        print('sql ----', sql)
        print('params ----', i.sql_params)
        print(i.replace_placeholder('%s'))


    def test_delete():
        d = DeleteImpl(TestModel)
        sql = d.delete().build()
        print('sql ----', sql)
        print(d.table_name)
        print(d.sql)


    def test_update():
        t = TestModel(id=1, name='张三')
        u = UpdateImpl(t)
        sql = u.update().build()
        print('sql ---', sql)
        print(u.table_name)
        print(u.sql)
        print(u.sql_params)


    def test_join():
        j = JoinImpl(TestModel, JoinImpl.JoinTypeEnum.join)
        sql = j.on(TestModel.id == TestModel.id, TestModel.name == '张3').build()
        print('sql ---', sql)
        print(j.table_name)
        print(j.sql)
        print(j.sql_params)


    test_where()
