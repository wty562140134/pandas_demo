from typing import Callable


class MyMetaClass(type):

    # def __new__(cls, name, bases, namespace):
    #     """
    #     元类使用__new__方式
    #
    #     Args:
    #         cls (): 需要通过此元类动态修改的类对象即class对象, 不需要手动传入, 在类使用metaclass=MyMetaClass的时候会自动将类对象传入
    #         name (): 动态修改的类对象的名称, 即类名
    #         bases (): 类对象所继承的所有父类
    #         namespace (): 类对象中所有的属性以及函数的字典
    #     """
    #     print('要修改的clss对象:', cls)
    #     print('要修改的clss对象类名:', name)
    #     print('要修改的clss对象继承所有父类:', bases)
    #     print('要修改的clss对象继承所有属性, 函数字典:', namespace)
    #     namespace['meta_class_func'] = MyMetaClass.meta_class_func
    #     return super(MyMetaClass, cls).__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        """
        元类使用__init__方式

        Args:
            cls (): 这里的cls是通过元类来创建的clss对象, 并不是通常类中的self实例, 在这个Demo中为MyBaseClass的class对象
            name (): 通过元类创建的class对象名
            bases (): 通过元类创建的class所继承的父类
            namespace (): 通过元类创建class对象所有属性
        """
        super(MyMetaClass, cls).__init__(name, bases, namespace)
        # 动态给通过元类创建对象添加一个函数
        cls.meta_class_func: Callable = cls.meta_class_func

    def meta_class_func(cls):
        print('这是元类增加方法', cls)


class MyBaseClass(metaclass=MyMetaClass):

    def say(self):
        print('不知道说什么。。。。')

    def __fun(self):
        print('私有__fun函数')


class MyClass(MyBaseClass):
    pass


if __name__ == '__main__':
    m = MyClass()
    m.say()
    m.meta_class_func()
