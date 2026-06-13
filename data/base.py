from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class KlineBar:
    seq: int
    ts_open: float
    open: float
    high: float
    low: float
    close: float
    volume: float
    closed: bool


def normalize_kline_bar(bar: KlineBar) -> KlineBar:
    from data.datetime_ts import ts_open_to_ms

    ts_ms = ts_open_to_ms(bar.ts_open)
    high = max(bar.high, bar.low)
    low = min(bar.high, bar.low)
    close = max(low, min(high, bar.close))
    if (
        high == bar.high
        and low == bar.low
        and close == bar.close
        and ts_ms == bar.ts_open
    ):
        return bar
    return KlineBar(
        seq=bar.seq,
        ts_open=ts_ms,
        open=bar.open,
        high=high,
        low=low,
        close=close,
        volume=bar.volume,
        closed=bar.closed,
    )


class DataSourceError(Exception):
    pass


class DataSourceTransientError(DataSourceError):
    pass


class DataSource(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def list_symbols(self) -> list[str]:
        pass

    @abstractmethod
    def supported_timeframes(self) -> list[str]:
        pass

    @abstractmethod
    def subscribe(self, symbol: str, timeframe: str) -> None:
        pass

    @abstractmethod
    def unsubscribe(self) -> None:
        pass

    @abstractmethod
    def latest_snapshot(self, n: int) -> list[KlineBar]:
        pass
