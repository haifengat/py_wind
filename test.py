#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/3/7
# @desc    : test

from py_wind.wind import Wind

if __name__ == '__main__':
    w = Wind()
    df = w.get_history_day('000001.SH', '2019-03-01')
    print(df)
    w.stop()