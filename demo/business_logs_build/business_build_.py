import abc
from typing import Generic, TypeVar, List, Dict, Union

T = TypeVar('T')


class NotReWriteException(Exception):
    pass


class AbstractBase(Generic[T], metaclass=abc.ABCMeta):
    pass


class AbstractBaseBusiness(AbstractBase):

    @abc.abstractmethod
    def build(self):
        """
        构建函数, 执行完所有必要函数后调用函数

        Returns:

        """
        pass


class BaseBusiness(AbstractBaseBusiness):

    # noinspection PyUnusedLocal
    def __init__(self, save_data: Union[List[Dict], Dict]):
        self.stop_step = False

    def build(self):
        raise NotReWriteException('函数verification_logical未重写')


class MyBusiness(BaseBusiness):

    def __init__(self, save_data: Union[List[Dict], Dict]):
        super().__init__(save_data)
        self.__save_data = save_data

    def build(self):
        self.stop_step = True
        return self.__save_data

    def step1(self):
        name = self.__save_data.get('name')
        if name == '赖总':
            self.__save_data['address'] = '北市区'
        print('step1')

    def step2(self):
        address = self.__save_data.get('address')
        if address == '北市区':
            self.__save_data['age'] = 25
            self.stop_step = True
        print('step2')

    def step3(self):
        if self.__save_data.get('age') == 25:
            self.__save_data['like'] = '会所'
        print('step3')

    def step4(self):
        if self.__save_data.get('like') == '会所':
            self.__save_data['game'] = '3P'
        print('step4')


class BusinessBuildManage:

    def __init__(self, business_instance: BaseBusiness):
        self.__build_func = None
        self.__business_instance = business_instance
        self.__step = 1

    def business_building(self):
        while True:
            try:
                step_func = self.__business_instance.__getattribute__('step{}'.format(self.__step))
                step_func()
                if self.__business_instance.__getattribute__('stop_step'):
                    self.__build_func = self.__business_instance.__getattribute__('build')
                    break
            except AttributeError as e:
                if str(e) == "'{}' object has no attribute 'step{}'".format(self.__business_instance.__class__.__name__,
                                                                            self.__step):
                    self.__build_func = self.__business_instance.__getattribute__('build')
                    break
                raise e
            self.__step += 1
        result = self.__build_func()
        return result


if __name__ == '__main__':
    b = MyBusiness({'name': '赖总'})
    print(BusinessBuildManage(b).business_building())
