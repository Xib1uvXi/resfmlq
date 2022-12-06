import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class CorrelationAnalyer:
    def corr(self, k1: pd.Series, k2: pd.Series) -> float:
        return np.corrcoef(k1.values, k2.values)[0, 1]

    def plot(self, df: pd.DataFrame, method: str = "all") -> None:
        fig = make_subplots(
            rows=1,
            cols=3 if method == "all" else 1,
            subplot_titles=(
                "皮尔逊积矩相关系数 (Pearson correlation coefficient)",
                "肯德尔等级相关系数 (Kendall rank correlation coefficient)",
                "斯皮尔曼等级相关系数 (Spearman's rank correlation coefficient)",
            )
            if method == "all"
            else ("皮尔逊积矩相关系数 (Pearson correlation coefficient)",)
            if method == "pearson"
            else ("肯德尔等级相关系数 (Kendall rank correlation coefficient)",)
            if method == "kendall"
            else ("斯皮尔曼等级相关系数 (Spearman's rank correlation coefficient)",),
        )

        def generate_heatmap(df: pd.DataFrame, col: int):
            fig.add_trace(
                go.Heatmap(
                    x=df.columns,
                    y=df.index,
                    z=np.array(df),
                    text=df.values,
                    texttemplate="%{text:.2f}",
                    colorscale=px.colors.diverging.RdBu,
                ),
                row=1,
                col=col,
            )

        if method == "all":
            generate_heatmap(df.corr(method="pearson"), 1)
            generate_heatmap(df.corr(method="kendall"), 2)
            generate_heatmap(df.corr(method="spearman"), 3)

        elif method == "pearson":
            generate_heatmap(df.corr(method="pearson"), 1)

        elif method == "kendall":
            generate_heatmap(df.corr(method="kendall"), 1)

        elif method == "spearman":
            generate_heatmap(df.corr(method="spearman"), 1)

        fig.update_layout(
            title="相关系数矩阵 (Correlation matrix)",
        )

        fig.show()
