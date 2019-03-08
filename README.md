# py_wind
wind 接口简易封装

## 环境需求
* python 3.6+

## 使用说明
    更多函数用法,详见函数说明.
    get_stock_ids       取板块的证券代码 BanKuai.A /SH /SZ
    get_history_day     取历史日线行情
    get_history_min     取历史分钟行情
    get_filter_stocks   取条件选股的结果
    sub_quote           订阅行情
    
### 示例
```python

from py_wind.wind import Wind, StockTick
import py_wind.stock_ids as ids

def OnTick(tick:StockTick):
    print(tick.__dict__)

if __name__ == '__main__':
    s = Wind()
    # 历史行情
    df = s.get_stock_ids(ids.BK_A) # 取板块构成
    print(df)
    df = s.get_history_min(ids.ZS_SH, '2019-01-01', period=5) # 取指数行情数据
    print(df)
    # 实时行情
    s.on_tick = OnTick
    s.sub_quote('000001.SZ')
    while input() != 'q':
        continue
    s.stop()

```

