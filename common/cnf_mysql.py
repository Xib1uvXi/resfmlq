import os.path
from datetime import datetime
from typing import Optional

import myloginpath
import pandas as pd
from pyarrow import feather

conf = myloginpath.parse("client")
conn = f"mysql://{conf['user']}:{conf['password']}@{conf['host']}/cfdata"


def get_close_prices(
    symbol: str, exhange: str, interval: str, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> pd.DataFrame:
    """获取收盘价格

    Args:
        symbol (str): 标的名称
        interval (str): 周期级别
        start (Optional[datetime], optional): 开始时间. Defaults to None.
        end (Optional[datetime], optional): 结束时间. Defaults to None.

    Returns:
        pd.DataFrame: 收盘价时间序列
    """

    filename = f"/tmp/cnf_prices_{symbol}_{interval}_{start}_{end}.feather"
    if os.path.exists(filename):
        return feather.read_feather(filename)

    sql = (
        "select b.datetime open_time, b.open_price open, b.high_price high, b.low_price low, b.close_price close, b.volume"
        f" from dbbardata b where b.symbol = '{symbol}' and b.exchange = '{exhange}' and b.`interval` = '{interval}'"
    )

    if start:
        sql += f" and b.datetime >= '{start}'"

    if end:
        sql += f" and b.datetime <= '{end}'"

    sql += " order by b.datetime asc"
    df = pd.read_sql(sql, conn, index_col=["open_time"])
    # df = df.tz_localize("Asia/Hong_Kong")

    feather.write_feather(df, filename)
    return df
