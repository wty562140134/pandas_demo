#!/usr/bin/python3  
# -*- coding: utf-8 -*-

"""
@Project      : sqlalchemy_test

@Email        : 562140134@qq.com

@Modify Time  : 2023-08-23 11:15

@Author       : Arthas

@Version      : 1.0

@IDE          : PyCharm


===============

@Description  :

===============
"""
import asyncio
from asyncio import sleep


class AsyncDemo:

    async def a(self):
        print('a start')
        await sleep(3)
        print('a over')

    async def b(self):
        print('b start')
        print('b over')

async def async_main():
    t = AsyncDemo()
    await asyncio.gather(
        t.a(),
        t.b()
    )



if __name__ == '__main__':
    asyncio.run(async_main())
