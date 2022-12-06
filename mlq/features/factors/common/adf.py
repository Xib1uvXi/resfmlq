from dataclasses import dataclass

import pandas as pd
from arch.unitroot import ADF


@dataclass
class ADFSttring:
    trend: str = "c"
    pvalue: float = 0.05
    show: bool = False


class ADFChecker:
    def __init__(self, data: pd.Series, settings: ADFSttring = ADFSttring()):
        self.data = data.dropna()
        self.settings = settings
        self.adf = ADF(self.data, trend=settings.trend)

    def is_stationary(self) -> None:
        result = self.adf.pvalue < self.settings.pvalue

        if (not result) and self.settings.show:
            print("The process contains a unit root")
            print(self.data.name, self.adf.summary().as_text())

        assert result, "The process contains a unit root"
