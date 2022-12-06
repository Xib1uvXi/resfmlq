import pandas as pd
import pandas_ta as ta

from mlq.features.factors.common.adf import ADFChecker


class RSIDiffFactor:
    timeperiod: int
    factor: pd.Series

    def __init__(self, timeperiod: int, diff: int):
        self.timeperiod = timeperiod
        self.diff = diff

    def name(self) -> str:
        return "rsi_diff_%d" % self.timeperiod

    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        self.factor = ta.rsi(df["close"], length=self.timeperiod)
        ADFChecker(self.factor).is_stationary()
        df[self.name()] = self.factor.diff(self.diff)
        return df
