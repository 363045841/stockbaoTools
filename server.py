from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from stock_service import get_stock_k_data, query_all_stock

app = FastAPI(title="股票数据API服务", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StockDataResponse(BaseModel):
    success: bool
    stock_code: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    data_count: int = 0
    data: list = []
    error_code: Optional[str] = None
    error_msg: Optional[str] = None


class StockListResponse(BaseModel):
    success: bool
    date: Optional[str] = None
    data_count: int = 0
    data: list = []
    error_code: Optional[str] = None
    error_msg: Optional[str] = None


@app.get("/")
def root():
    return {"message": "股票数据API服务", "docs": "/docs"}


@app.get("/api/stock/kdata", response_model=StockDataResponse)
def stock_k_data(
    stock_code: str = Query(..., description="股票代码，如 sh.600000"),
    start_date: str = Query(..., description="开始日期，格式 2024-07-01"),
    end_date: str = Query(..., description="结束日期，格式 2024-12-31"),
    frequency: str = Query("d", description="数据频率: d=日, w=周, m=月, 5=5分钟, 15=15分钟, 30=30分钟, 60=60分钟"),
    adjustflag: str = Query("3", description="复权类型: 1=后复权, 2=前复权, 3=不复权")
):
    """
    获取股票历史K线数据
    """
    result = get_stock_k_data(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        adjustflag=adjustflag
    )
    return result


@app.get("/api/stock/list", response_model=StockListResponse)
def stock_list(date: Optional[str] = Query(None, description="查询日期，格式 2024-07-01")):
    """
    获取所有股票列表
    """
    result = query_all_stock(date=date)
    return result


@app.get("/api/stock/query")
def stock_query(
    stock_code: str = Query(..., description="股票代码，如 sh.600000"),
    days: int = Query(30, description="查询天数")
):
    """
    快捷查询最近N天的股票数据
    """
    from datetime import datetime, timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    result = get_stock_k_data(
        stock_code=stock_code,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        frequency="d",
        adjustflag="3"
    )
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
