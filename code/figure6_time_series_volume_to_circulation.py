import requests
import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure

# Create a api_key.py file in the same directory and add your CMC API key
from api_key import CMC_API_KEY
from utils import fetch_cmc_data


def plot_ts_speculative_ratio(
    start_date=datetime.datetime(2019, 1, 1), end_date=datetime.datetime(2023, 3, 31)
):
    # Fetch daily USDC, USDT, and BUSD market cap data from CMC
    usdc_data = fetch_cmc_data("USDC").loc[start_date:end_date]
    usdt_data = fetch_cmc_data("USDT").loc[start_date:end_date]
    busd_data = fetch_cmc_data("BUSD").loc[start_date:end_date]

    ts_data = usdt_data.merge(busd_data, left_index=True, right_index=True, how="outer")
    ts_data.fillna(0, inplace=True)
    ts_data["ts_market_cap"] = ts_data["USDT_market_cap"] + ts_data["BUSD_market_cap"]
    ts_data["ts_volume"] = ts_data["USDT_volume"] + ts_data["BUSD_volume"]

    ts_data=ts_data.merge(usdc_data,left_index=True,right_index=True, how='outer')
    dtplot=ts_data.resample('Y').mean().assign(Trading_Stablecoins=lambda x: x.ts_volume/x.ts_market_cap,
                                    USDC=lambda x:x.USDC_volume/x.USDC_market_cap)
    dtplot.index=dtplot.index.year
    combined=dtplot[['USDC','Trading_Stablecoins']].rename(columns={'Trading_Stablecoins':'Trading Stablecoins'})

    figure(figsize=(18, 12), dpi=300)
    ax = plt.axes()
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)

    color_dict = {"USDC": "#2775ca", "Trading Stablecoins": "#c7c5d1"}
    combined = combined[["USDC", "Trading Stablecoins"]]

    combined.plot(
        kind="bar",
        ax=ax,
        color=list(color_dict.values()),
        width=0.75,
        legend=True,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=0, fontsize=30)
    plt.xticks(fontsize=25)
    plt.legend(bbox_to_anchor=(0.5, -0.05), loc="upper center", ncol=2, fontsize=30)

    plt.savefig("../output/Figure6.png", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_ts_speculative_ratio()
