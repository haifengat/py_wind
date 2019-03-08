#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '20181017'

from datetime import datetime, timedelta
import sys
from color_log import Logger
import pandas as pd
from pandas import DataFrame
from WindPy import w
from enum import Enum
from .stock_tick import StockTick
from .stock_ids import *


class Wind(object):
    """Wind"""

    def __init__(self):
        """"""
        self.log = Logger()
        self.ticks = {}

        w.start()
        if not w.isconnected():
            print('login.')
            w.stop()
            raise Exception('登录失败')

    def get_stock_ids(self, type: str) -> DataFrame:
        """取板块的证券代码

        :param type: 板块名称
        :return: 股票代码
        """
        data = w.wset('sectorconstituent', f'sectorid={type}')
        df: DataFrame = DataFrame(data.Data).T
        df.columns = data.Fields
        df.drop(columns=[data.Fields[0]], axis=1, inplace=True)
        return df

    def get_history_day(self, stock_id: str, start_day: str, end_day: str = '') -> DataFrame:
        """取历史日线行情

        :param stock_id: 证券代码
        :param start_day: (含)起始日期 yyyy-mm-dd
        :param end_day: (含)结束日期 yyyy-mm-dd 默认:前一日
        :return: index-日期 fields-pre_close,open,high,low,close,volume,amt
        """
        data = w.wsd(stock_id, "pre_close,open,high,low,close,volume,amt", start_day, end_day if end_day != '' else datetime.today() - timedelta(days=1))
        df: DataFrame = DataFrame(data.Data, columns=data.Times, index=data.Fields).T  # .T 行列转换
        return df

    def get_history_min(self, stock_id: str, start_day: str, end_day: str = '', period=1) -> DataFrame:
        """取历史分钟行情

        :param stock_id: 证券代码
        :param start_day: 起始日期 yyyy-mm-dd
        :param end_day: 结束日期 yyyy-mm-dd 默认:前一日
        :param period: 周期 默认 1
        :return: index-日期 fields-pre_close,open,high,low,close,volume,amt
        """
        data = w.wsi(stock_id, "open,high,low,close,volume,amt", start_day, end_day if end_day != '' else datetime.today() - timedelta(days=1), f'BarSize={period}')
        df: DataFrame = DataFrame(data.Data, columns=data.Times, index=data.Fields).T  # .T 行列转换
        df.rename(columns={'amount': 'amt'}, inplace=True)
        return df

    def get_filter_stocks(self, filtername) -> list:
        """取条件选股的结果

        :param filtername: 条件选股方案名称
        :return: 股票代码列表
        """
        data = w.weqs('股本过滤')
        return data.Codes

    def stop(self):
        """"""
        w.cancelRequest(0)
        w.stop()

    def sub_quote(self, stock_id: str):
        """订阅行情

        :param stock_id:股票代码
        :return:
        """
        w.wsq(stock_id, 'rt_date,rt_time,rt_high,rt_last,rt_last_vol,rt_latest,rt_pct_chg,rt_chg,rt_high_limit,rt_low_limit,rt_trade_status,rt_ask1,rt_bid1,rt_bsize1,rt_asize1,rt_ask2,rt_bid2,rt_bsize2,rt_asize2,rt_ask3,rt_bid3,rt_bsize3,rt_asize3,rt_ask4,rt_bid4,rt_bsize4,rt_asize4,rt_ask5,rt_bid5,rt_bsize5,rt_asize5', func=self._on_tick)

    def _on_tick(self, indata):
        """实时行情返回
            # indata的数据结构如下：
            # indata.ErrorCode 错误码，如果为0表示运行正常
            # indata.StateCode 状态字段，使用时无需处理
            # indata.RequestID 存放对应wsq请求的RequestID
            # indata.Codes 存放行情对应的code
            # indata.Fields 存放行情数据对应的指标
            # indata.Times 存放本地时间，注意这个不是行情对应的时间，要获取行情对应的时间，请订阅rt_time指标
            # indata.Data 存放行情数据

        :param indata: 行情数据
        :return:
        """
        if indata.ErrorCode != 0:
            return
        stock_id = indata.Codes[0]
        if stock_id not in self.ticks:
            self.ticks[stock_id] = StockTick()
            self.ticks[stock_id].StockId = stock_id
        tick: StockTick = self.ticks[stock_id]
        tick.DATE = int(indata.Data[indata.Fields.index('RT_DATE')][0] if 'RT_DATE' in indata.Fields else tick.DATE)
        tick.TIME = int(indata.Data[indata.Fields.index('RT_TIME')][0] if 'RT_TIME' in indata.Fields else tick.TIME)
        tick.HIGH = indata.Data[indata.Fields.index('RT_HIGH')][0] if 'RT_HIGH' in indata.Fields else tick.HIGH
        tick.LAST = indata.Data[indata.Fields.index('RT_LAST')][0] if 'RT_LAST' in indata.Fields else tick.LAST
        tick.LAST_VOL = indata.Data[indata.Fields.index('RT_LAST_VOL')][0] if 'RT_LAST_VOL' in indata.Fields else tick.LAST_VOL
        tick.LATEST = indata.Data[indata.Fields.index('RT_LATEST')][0] if 'RT_LATEST' in indata.Fields else tick.LATEST
        tick.PCT_CHG = indata.Data[indata.Fields.index('RT_PCT_CHG')][0] if 'RT_PCT_CHG' in indata.Fields else tick.PCT_CHG
        tick.CHG = indata.Data[indata.Fields.index('RT_CHG')][0] if 'RT_CHG' in indata.Fields else tick.CHG
        tick.HIGH_LIMIT = indata.Data[indata.Fields.index('RT_HIGH_LIMIT')][0] if 'RT_HIGH_LIMIT' in indata.Fields else tick.HIGH_LIMIT
        tick.LOW_LIMIT = indata.Data[indata.Fields.index('RT_LOW_LIMIT')][0] if 'RT_LOW_LIMIT' in indata.Fields else tick.LOW_LIMIT
        tick.TRADE_STATUS = indata.Data[indata.Fields.index('RT_TRADE_STATUS')][0] if 'RT_TRADE_STATUS' in indata.Fields else tick.TRADE_STATUS
        tick.ASK1 = indata.Data[indata.Fields.index('RT_ASK1')][0] if 'RT_ASK1' in indata.Fields else tick.ASK1
        tick.BID1 = indata.Data[indata.Fields.index('RT_BID1')][0] if 'RT_BID1' in indata.Fields else tick.BID1
        tick.BSIZE1 = indata.Data[indata.Fields.index('RT_BSIZE1')][0] if 'RT_BSIZE1' in indata.Fields else tick.BSIZE1
        tick.ASIZE1 = indata.Data[indata.Fields.index('RT_ASIZE1')][0] if 'RT_ASIZE1' in indata.Fields else tick.ASIZE1
        tick.ASK2 = indata.Data[indata.Fields.index('RT_ASK2')][0] if 'RT_ASK2' in indata.Fields else tick.ASK2
        tick.BID2 = indata.Data[indata.Fields.index('RT_BID2')][0] if 'RT_BID2' in indata.Fields else tick.BID2
        tick.BSIZE2 = indata.Data[indata.Fields.index('RT_BSIZE2')][0] if 'RT_BSIZE2' in indata.Fields else tick.BSIZE2
        tick.ASIZE2 = indata.Data[indata.Fields.index('RT_ASIZE2')][0] if 'RT_ASIZE2' in indata.Fields else tick.ASIZE2
        tick.ASK3 = indata.Data[indata.Fields.index('RT_ASK3')][0] if 'RT_ASK3' in indata.Fields else tick.ASK3
        tick.BID3 = indata.Data[indata.Fields.index('RT_BID3')][0] if 'RT_BID3' in indata.Fields else tick.BID3
        tick.BSIZE3 = indata.Data[indata.Fields.index('RT_BSIZE3')][0] if 'RT_BSIZE3' in indata.Fields else tick.BSIZE3
        tick.ASIZE3 = indata.Data[indata.Fields.index('RT_ASIZE3')][0] if 'RT_ASIZE3' in indata.Fields else tick.ASIZE3
        tick.ASK4 = indata.Data[indata.Fields.index('RT_ASK4')][0] if 'RT_ASK4' in indata.Fields else tick.ASK4
        tick.BID4 = indata.Data[indata.Fields.index('RT_BID4')][0] if 'RT_BID4' in indata.Fields else tick.BID4
        tick.BSIZE4 = indata.Data[indata.Fields.index('RT_BSIZE4')][0] if 'RT_BSIZE4' in indata.Fields else tick.BSIZE4
        tick.ASIZE4 = indata.Data[indata.Fields.index('RT_ASIZE4')][0] if 'RT_ASIZE4' in indata.Fields else tick.ASIZE4
        tick.ASK5 = indata.Data[indata.Fields.index('RT_ASK5')][0] if 'RT_ASK5' in indata.Fields else tick.ASK5
        tick.BID5 = indata.Data[indata.Fields.index('RT_BID5')][0] if 'RT_BID5' in indata.Fields else tick.BID5
        tick.BSIZE5 = indata.Data[indata.Fields.index('RT_BSIZE5')][0] if 'RT_BSIZE5' in indata.Fields else tick.BSIZE5
        tick.ASIZE5 = indata.Data[indata.Fields.index('RT_ASIZE5')][0] if 'RT_ASIZE5' in indata.Fields else tick.ASIZE5

        self.on_tick(tick)

    def on_tick(self, tick: StockTick):
        """重写函数获取实时行情

        :param tick 分笔行情
        :return:
        """
        pass
