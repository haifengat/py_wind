#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/3/7
# @desc    : tick of stock

class StockTick(object):
    """股票分笔行情"""

    def __init__(self):
        """"""
        self.StockId: str = ''
        '''股票代码'''
        self.DATE: int = ''
        '''交易日:yyyyMMdd'''
        self.TIME: int = 0
        '''时间:hhmmss'''
        self.HIGH = .0
        '''当日最高'''
        self.LAST = .0
        '''最新'''
        self.LAST_VOL = .0
        '''成交量'''
        self.LATEST = .0
        self.PCT_CHG = .0
        self.CHG = .0
        self.HIGH_LIMIT = .0
        self.LOW_LIMIT = .0
        self.TRADE_STATUS = .0
        ''' trade_status: 未知-0  可交易-1  休市/暂停交易-2 收盘-3  集合竞价-4  暂停交易(深交所停牌/熔断)-5  盘前交易-8  盘后交易-9  期权波动性中断-10  可恢复熔断-11  不可恢复熔断-12'''
        self.ASK1 = .0
        self.BID1 = .0
        self.BSIZE1 = .0
        self.ASIZE1 = .0
        self.ASK2 = .0
        self.BID2 = .0
        self.BSIZE2 = .0
        self.ASIZE2 = .0
        self.ASK3 = .0
        self.BID3 = .0
        self.BSIZE3 = .0
        self.ASIZE3 = .0
        self.ASK4 = .0
        self.BID4 = .0
        self.BSIZE4 = .0
        self.ASIZE4 = .0
        self.ASK5 = .0
        self.BID5 = .0
        self.BSIZE5 = .0
        self.ASIZE5 = .0
