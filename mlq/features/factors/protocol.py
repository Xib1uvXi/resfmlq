from typing import Protocol

import pandas as pd


class FactorExtractor(Protocol):
    def name(self) -> str:
        ...

    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        ...
