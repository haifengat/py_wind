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


class Wind(object):
    """Wind"""

    def __init__(self):
        """"""
        self.log = Logger()

        w.start()
        if not w.isconnected():
            print('login.')
            w.stop()
            raise Exception('登录失败')

    def get_history_day(self, stock_id: str, start_day: str, end_day: str = '') -> DataFrame:
        """取历史日线行情

        :param stock_id: 证券代码
        :param start_day: 起始日期 yyyy-mm-dd
        :param end_day: 结束日期 yyyy-mm-dd 默认:前一日
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
        date = int(indata.Data[indata.Fields.index('rt_date'.upper())][0])
        time = int(indata.Data[indata.Fields.index('rt_time'.upper())][0])
        high = indata.Data[indata.Fields.index('rt_high'.upper())][0]
        last = indata.Data[indata.Fields.index('rt_last'.upper())][0]
        last_vol = indata.Data[indata.Fields.index('rt_last_vol'.upper())][0]
        latest = indata.Data[indata.Fields.index('rt_latest'.upper())][0]
        pct_chg = indata.Data[indata.Fields.index('rt_pct_chg'.upper())][0]
        chg = indata.Data[indata.Fields.index('rt_chg'.upper())][0]
        high_limit = indata.Data[indata.Fields.index('rt_high_limit'.upper())][0]
        low_limit = indata.Data[indata.Fields.index('rt_low_limit'.upper())][0]
        trade_status = indata.Data[indata.Fields.index('rt_trade_status'.upper())][0]
        ask1 = indata.Data[indata.Fields.index('rt_ask1'.upper())][0]
        bid1 = indata.Data[indata.Fields.index('rt_bid1'.upper())][0]
        bsize1 = indata.Data[indata.Fields.index('rt_bsize1'.upper())][0]
        asize1 = indata.Data[indata.Fields.index('rt_asize1'.upper())][0]
        ask2 = indata.Data[indata.Fields.index('rt_ask2'.upper())][0]
        bid2 = indata.Data[indata.Fields.index('rt_bid2'.upper())][0]
        bsize2 = indata.Data[indata.Fields.index('rt_bsize2'.upper())][0]
        asize2 = indata.Data[indata.Fields.index('rt_asize2'.upper())][0]
        ask3 = indata.Data[indata.Fields.index('rt_ask3'.upper())][0]
        bid3 = indata.Data[indata.Fields.index('rt_bid3'.upper())][0]
        bsize3 = indata.Data[indata.Fields.index('rt_bsize3'.upper())][0]
        asize3 = indata.Data[indata.Fields.index('rt_asize3'.upper())][0]
        ask4 = indata.Data[indata.Fields.index('rt_ask4'.upper())][0]
        bid4 = indata.Data[indata.Fields.index('rt_bid4'.upper())][0]
        bsize4 = indata.Data[indata.Fields.index('rt_bsize4'.upper())][0]
        asize4 = indata.Data[indata.Fields.index('rt_asize4'.upper())][0]
        ask5 = indata.Data[indata.Fields.index('rt_ask5'.upper())][0]
        bid5 = indata.Data[indata.Fields.index('rt_bid5'.upper())][0]
        bsize5 = indata.Data[indata.Fields.index('rt_bsize5'.upper())][0]
        asize5 = indata.Data[indata.Fields.index('rt_asize5'.upper())][0]
        self.on_tick(indata.Codes[0], date, time, high, last, last_vol, latest, pct_chg, chg, high_limit, low_limit, trade_status, ask1, bid1, bsize1, asize1, ask2, bid2, bsize2, asize2, ask3, bid3, bsize3, asize3, ask4, bid4, bsize4, asize4, ask5, bid5, bsize5, asize5)

    def on_tick(self, stock_id: str, date, time, high, last, last_vol, latest, pct_chg, chg, high_limit, low_limit, trade_status, ask1, bid1, bsize1, asize1, ask2, bid2, bsize2, asize2, ask3, bid3, bsize3, asize3, ask4, bid4, bsize4, asize4, ask5, bid5, bsize5, asize5):
        """重写函数获取实时行情

        :param stock_id:
        :param date:
        :param time:
        :param high:
        :param last:
        :param last_vol:
        :param latest:
        :param pct_chg:
        :param chg:
        :param high_limit:
        :param low_limit:
        :param trade_status: 未知-0  可交易-1  休市/暂停交易-2 收盘-3  集合竞价-4  暂停交易(深交所停牌/熔断)-5  盘前交易-8  盘后交易-9  期权波动性中断-10  可恢复熔断-11  不可恢复熔断-12
        :param ask1:
        :param bid1:
        :param bsize1:
        :param asize1:
        :param ask2:
        :param bid2:
        :param bsize2:
        :param asize2:
        :param ask3:
        :param bid3:
        :param bsize3:
        :param asize3:
        :param ask4:
        :param bid4:
        :param bsize4:
        :param asize4:
        :param ask5:
        :param bid5:
        :param bsize5:
        :param asize5:
        :return:
        """
        print(f'{stock_id}, {date}, {time}, {high}, {last}, {last_vol}, {latest}, {pct_chg}, {chg}, {high_limit}, {low_limit}, {trade_status}, {ask1}, {bid1}, {bsize1}, {asize1}, {ask2}, {bid2}, {bsize2}, {asize2}, {ask3}, {bid3}, {bsize3}, {asize3}, {ask4}, {bid4}, {bsize4}, {asize4}, {ask5}, {bid5}, {bsize5}, {asize5}')


if __name__ == '__main__':
    s = Wind()
    # df = s.get_history_min('000001.SZ', '2019-01-01', period=5)
    # print(df)
    s.sub_quote('000001.SZ')
    while input() != 'q':
        continue
    s.stop()
