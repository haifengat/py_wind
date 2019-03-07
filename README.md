# py_wind
wind 接口简易封装

## 环境需求
* python 3.6+

## 使用说明
    更多函数用法,详见函数说明.
    
### 示例
```python
from py_wind.wind import Wind

if __name__ == '__main__':
    w = Wind()
    df = w.get_history_day('000001.SH', '2019-03-01')
    print(df)
    w.stop()
```

