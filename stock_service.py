import baostock as bs
import pandas as pd
from typing import Optional


def get_stock_k_data(
    stock_code: str,
    start_date: str,
    end_date: str,
    frequency: str = "d",
    adjustflag: str = "3",
    fields: Optional[str] = None
) -> dict:
    """
    获取股票历史K线数据

    Args:
        stock_code: 股票代码，如 "sh.600000"
        start_date: 开始日期，格式 "2024-07-01"
        end_date: 结束日期，格式 "2024-12-31"
        frequency: 数据频率，d=日 k线, w=周, m=月, 5=5分钟, 15=15分钟, 30=30分钟, 60=60分钟
        adjustflag: 复权类型，1=后复权, 2=前复权, 3=不复权
        fields: 查询字段，默认使用全部字段

    Returns:
        dict: 包含股票数据的字典
    """
    if fields is None:
        fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

    # 登陆系统
    lg = bs.login()
    if lg.error_code != '0':
        return {
            "success": False,
            "error_code": lg.error_code,
            "error_msg": lg.error_msg
        }

    try:
        # 查询数据
        rs = bs.query_history_k_data_plus(
            stock_code,
            fields,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )

        if rs is None:
            return {
                "success": False,
                "error_code": "-1",
                "error_msg": "baostock返回空数据，可能是网络问题或股票代码不存在"
            }

        if rs.error_code != '0':
            return {
                "success": False,
                "error_code": rs.error_code,
                "error_msg": rs.error_msg
            }

        # 获取数据
        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())

        # 转换为DataFrame再转为字典列表
        df = pd.DataFrame(data_list, columns=rs.fields)

        return {
            "success": True,
            "stock_code": stock_code,
            "start_date": start_date,
            "end_date": end_date,
            "data_count": len(data_list),
            "data": df.to_dict(orient='records')
        }

    finally:
        # 登出系统
        bs.logout()


def query_all_stock(date: str = None) -> dict:
    """
    获取所有股票列表

    Args:
        date: 查询日期，格式 "2024-07-01"，默认为空

    Returns:
        dict: 包含股票列表的字典
    """
    lg = bs.login()
    if lg.error_code != '0':
        return {
            "success": False,
            "error_code": lg.error_code,
            "error_msg": lg.error_msg
        }

    try:
        rs = bs.query_all_stock(day=date)

        if rs is None:
            return {
                "success": False,
                "error_code": "-1",
                "error_msg": "baostock返回空数据，可能是网络问题"
            }

        if rs.error_code != '0':
            return {
                "success": False,
                "error_code": rs.error_code,
                "error_msg": rs.error_msg
            }

        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())

        df = pd.DataFrame(data_list, columns=rs.fields)

        return {
            "success": True,
            "date": date,
            "data_count": len(data_list),
            "data": df.to_dict(orient='records')
        }

    finally:
        bs.logout()
