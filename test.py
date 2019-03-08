#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/3/7
# @desc    : test

from py_wind.wind import Wind, StockTick
import py_wind.stock_ids as ids

def OnTick(tick:StockTick):
    print(tick.__dict__)

if __name__ == '__main__':
    s = Wind()
    # 历史行情
    df = s.get_stock_ids(ids.BK_A)
    print(df)
    df = s.get_history_min(ids.ZS_SH, '2019-01-01', period=5)
    print(df)
    # 实时行情
    s.on_tick = OnTick
    s.sub_quote('000001.SZ')
    while input() != 'q':
        continue
    s.stop()
