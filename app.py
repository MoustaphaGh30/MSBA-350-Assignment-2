import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Stock Returns Analysis Dashboard")


DATA_DIR = "data"
data = pd.read_csv(f"{DATA_DIR}/data_with_returns.csv", index_col=0, parse_dates=True)
df_rv = pd.read_csv(f"{DATA_DIR}/realized_volatility.csv", index_col=0, parse_dates=True)
monthly_returns = pd.read_csv(f"{DATA_DIR}/monthly_returns_with_inflation_adjusted.csv", index_col=0, parse_dates=True)
eth_df=pd.read_csv(f"{DATA_DIR}/ETHUSDT_last_1000_trades.csv")
ada_df=pd.read_csv(f'{DATA_DIR}/ADAUSDT_last_1000_trades.csv')
matic_df=pd.read_csv(f'{DATA_DIR}/MATICUSDT_last_1000_trades.csv')

stocks = ['FLG', 'HWKN', 'HON', 'GS', 'EA', 'F', 'GOOGL', 'GE', 'HD', 'HLT']
crypto_files = {
    "ETH": eth_df,
    "ADA": ada_df,
    "MATIC": matic_df
}

plot_option = st.sidebar.selectbox(
    "Select Plot Option",
    [
        "Simple vs Log Returns",
        "Annualized Volatility Comparison",
        "Adjusted vs Non-Adjusted Returns",
        "Crypto Bars Analysis"
    ]
)


if plot_option == "Simple vs Log Returns":
    selected_stock = st.sidebar.selectbox("Select Stock", stocks)
    simple_col = selected_stock + "_simple.return"
    log_col = selected_stock + "_log.return"
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharex=True)
    
    axes[0].plot(data.index, (data[simple_col] * 100).round(2), label="Simple Return", color="blue", alpha=0.7)
    axes[0].set_title(f"Simple Returns for {selected_stock}")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Return (%)")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.6)
    
    axes[1].plot(data.index, (data[log_col] * 100).round(2), label="Log Return", color="red", alpha=0.7)
    axes[1].set_title(f"Log Returns for {selected_stock}")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Return (%)")
    axes[1].legend()
    axes[1].grid(True, linestyle="--", alpha=0.6)
    
    st.pyplot(fig)
    
    comments = {
        "FLG": "FLG's return range reflects moderate volatility typical of the mortgage banking sector, bolstered by steady lending performance despite occasional regulatory scrutiny.",
        "HWKN": "HWKN's return range has been influenced by operational restructuring and competitive market pressures, leading to wider fluctuations in investor sentiment.",
        "HON": "HON's tight return range underscores its stable industrial performance and diversified product portfolio that helps mitigate broader economic volatility.",
        "GS": "GS's broader return range mirrors the inherent volatility in the financial sector, driven by market fluctuations, regulatory shifts, and global economic uncertainties.",
        "EA": "EA's sporadic return spikes capture the dynamic nature of the gaming industry, with investor reactions tied to blockbuster releases and evolving consumer trends.",
        "F": "F's fluctuating returns highlight the cyclical challenges in the automotive sector, influenced by supply chain disruptions, intense competition, and shifting consumer demand.",
        "GOOGL": "GOOGL's minimal return range underscores its robust growth and diversified revenue streams, which help stabilize performance amid tech sector headwinds.",
        "GE": "GE's notable return variance reflects ongoing restructuring efforts and shifts in its industrial segments, periodically unsettling investor sentiment.",
        "HD": "HD's steady yet occasionally spiking returns mirror the resilience of the home improvement sector and strong consumer demand in housing markets.",
        "HLT": "HLT's return volatility is emblematic of the hospitality sector's sensitivity to global travel trends and economic cycles, especially during recovery phases."
    }
    
    comment_text = comments.get(selected_stock, "No comment available for this stock.")
    
    st.markdown(f"<div style='font-size:20px; font-weight:bold; margin-top:20px;'>{comment_text}</div>", unsafe_allow_html=True)



elif plot_option == "Annualized Volatility Comparison":
    selected_stocks = st.sidebar.multiselect("Select Stocks", stocks, default=stocks)
    vol_cols = [s + "_rv" for s in selected_stocks if s + "_rv" in df_rv.columns]
    
    if len(vol_cols) == 0:
        st.write("No volatility data available for the selected stocks.")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for stock in vol_cols:
            ax.plot(df_rv.index, df_rv[stock], label=stock.removesuffix("_rv"))
        
        ax.set_title("Annualized Volatility Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volatility")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        
        st.pyplot(fig)
        
        # Display tailored comments in larger font using markdown and HTML
        comments_html = """
        <div style='font-size:20px;'>
          <ul>
            <li><strong>Volatility Comparison:</strong> Among the selected stocks, Ford (F) exhibits the highest volatility—reflecting cyclical challenges and supply chain disruptions in the automotive sector—while companies like Honeywell (HON) and Home Depot (HD) show more stable behavior.</li>
            <li><strong>Mid-2020 Spike:</strong> The common spike in volatility around mid-2020 is attributable to the COVID‑19 pandemic, which triggered widespread economic uncertainty, supply chain disruptions, and industry-specific challenges (such as layoffs and operational adjustments) across multiple sectors.</li>
            <li><strong>Flagstar’s CRE Impact:</strong> In Q3 2024, Flagstar experienced a dramatic rise in net charge-offs to $240 million, largely due to mounting stress in its commercial real estate portfolio, reflecting broader challenges faced by U.S. regional banks in the sector.</li>
          </ul>
        </div>
        """
        st.markdown(comments_html, unsafe_allow_html=True)




elif plot_option == "Adjusted vs Non-Adjusted Returns":
    selected_stock = st.sidebar.selectbox("Select Stock", stocks)
    simple_col = selected_stock + "_simple.return"
    adjusted_col = selected_stock + "_real.return"
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_returns.index, monthly_returns[simple_col]*100, label="Non-Adjusted Return")
    ax.plot(monthly_returns.index, monthly_returns[adjusted_col]*100, label="Inflation Adjusted Return")
    ax.set_title(f"Monthly Adjusted vs Non-Adjusted Returns for {selected_stock}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Return")
    ax.legend()
    st.pyplot(fig)
    
    comments_html = """
    <div style='font-size:20px;'>
      <ul>
        <li><strong>Notable Trends:</strong> Stocks in sectors that are more economically sensitive—such as automotive (F) and hospitality (HLT)—show a more pronounced gap between simple and adjusted returns, while technology (GOOGL) and gaming (EA) stocks display minimal differences, indicating that their robust growth has largely outpaced inflation.</li>
      </ul>
    </div>
    """
    st.markdown(comments_html, unsafe_allow_html=True)

elif plot_option == "Crypto Bars Analysis":
    st.title("Crypto Bars Analysis")
    
    crypto = st.sidebar.selectbox("Select Cryptocurrency", list(crypto_files.keys()))
    
    bar_option = st.sidebar.selectbox("Select Bar Type", 
                                      ["All Bars", "Price Bars", "Tick Bars", "Volume Bars", "Dollar Bars"])
    
    tick_options = [20, 30, 50]
    tick_size = st.sidebar.selectbox("Tick Bar Count", tick_options)
    
    price_time_options = {"1 Minute": "1T", "5 Minutes": "5T", "15 Minutes": "15T"}
    price_interval_label = st.sidebar.selectbox("Price Bar Time Frame", list(price_time_options.keys()))
    price_interval = price_time_options[price_interval_label]
    
    volume_options = [10, 30, 70]
    volume_threshold = st.sidebar.selectbox("Volume Bar Threshold", volume_options)
    
    dollar_options = [10000, 20000, 50000]
    dollar_threshold = st.sidebar.selectbox("Dollar Bar Threshold", dollar_options)
    
    df = crypto_files[crypto].copy()
    
    df["time"] = pd.to_datetime(df["time"])
    df["price"] = df["price"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["dollar_value"] = df["price"] * df["volume"]
    
    # --------------------
    # Price Bars: use resample to aggregate by time.
    df_price = df.resample(price_interval, on="time").agg({"price": ["first", "max", "min", "last"]})
    df_price.columns = ["Open", "High", "Low", "Close"]
    
    # --------------------
    # Tick Bars: group by tick size and aggregate the time as the last timestamp.
    df_tick = df.groupby(df.index // tick_size).agg({
        "time": "last",          # You can also use "first" if preferred.
        "price": ["first", "max", "min", "last"]
    })
    df_tick.columns = ["Time", "Open", "High", "Low", "Close"]
    df_tick = df_tick.set_index("Time")
    
    # --------------------
    # Volume Bars: calculate cumulative volume and group by threshold,
    # then aggregate time as the last timestamp in each group.
    df["cumulative_volume"] = df["volume"].cumsum()
    df_volume = df.groupby(df["cumulative_volume"] // volume_threshold).agg({
        "time": "last",
        "price": ["first", "max", "min", "last"]
    })
    df_volume.columns = ["Time", "Open", "High", "Low", "Close"]
    df_volume = df_volume.set_index("Time")
    
    # --------------------
    # Dollar Bars: calculate cumulative dollar value and group by threshold,
    # then aggregate time as the last timestamp in each group.
    df["cumulative_dollar"] = df["dollar_value"].cumsum()
    df_dollar = df.groupby(df["cumulative_dollar"] // dollar_threshold).agg({
        "time": "last",
        "price": ["first", "max", "min", "last"]
    })
    df_dollar.columns = ["Time", "Open", "High", "Low", "Close"]
    df_dollar = df_dollar.set_index("Time")
    
    # --------------------
    # Plotting
    if bar_option == "All Bars":
        fig, axes = plt.subplots(2, 2, figsize=(17, 12))
        fig.suptitle(f"{crypto} - Bars Analysis", fontsize=16)
        
        # Price Bars (timestamp x-axis from resample)
        axes[0, 0].plot(df_price.index, df_price["Close"], label=f"Price Bars ({price_interval_label})")
        axes[0, 0].set_title(f"Price Bars ({price_interval_label})")
        axes[0, 0].legend()
        
        # Tick Bars (with timestamp index)
        axes[0, 1].plot(df_tick.index, df_tick["Close"], label=f"Tick Bars (Every {tick_size} Trades)", color="orange")
        axes[0, 1].set_title(f"Tick Bars (Every {tick_size} Trades)")
        axes[0, 1].legend()
        
        # Volume Bars (with timestamp index)
        axes[1, 0].plot(df_volume.index, df_volume["Close"], label=f"Volume Bars (Every {volume_threshold} Volume)", color="green")
        axes[1, 0].set_title(f"Volume Bars (Every {volume_threshold} Volume)")
        axes[1, 0].legend()
        
        # Dollar Bars (with timestamp index)
        axes[1, 1].plot(df_dollar.index, df_dollar["Close"], label=f"Dollar Bars (Every {dollar_threshold} USDT)", color="red")
        axes[1, 1].set_title(f"Dollar Bars (Every {dollar_threshold} USDT)")
        axes[1, 1].legend()
        
        st.pyplot(fig)
        
        # Display comments for all bar types
        st.write("**Tick Bars Comments:**")
        st.write("- **ETH:** ETH's tick bars change quickly, showing high liquidity and fast trading bursts.")
        st.write("- **ADA:** ADA's tick bars are less frequent but have bigger price swings, likely due to lower liquidity and occasional bursts.")
        st.write("- **MATIC:** MATIC's tick bars steadily rise with mild changes, suggesting gradual investor interest.")
        
        st.write("**Price Bars Comments:**")
        st.write("- **MATIC:** MATIC's price bars are sparse with gaps, indicating trading happens only at certain times, though the trend is upward.")
        st.write("- **ADA:** ADA's 15-minute price bars are smooth and show a general drop, perhaps due to consistent sell pressure.")
        st.write("- **ETH:** ETH's price bars are mostly continuous with one gap and high ups and downs, reflecting a bullish trend with rapid fluctuations.")
        
        st.write("**Volume Bars Comments:**")
        st.write("- **ETH:** ETH's volume bars stay mostly flat with small jumps at a threshold of 10, meaning high trade frequency smooths volume changes.")
        st.write("- **ADA:** ADA's volume bars show clear fluctuations at a threshold of 10, indicating even small volumes make a difference due to lower liquidity.")
        st.write("- **MATIC:** MATIC's volume bars display distinct spikes at 10, capturing sudden bursts of trading activity.")
        
        st.write("**Dollar Bars Comments (using 10000 USDT):**")
        st.write("- **MATIC:** MATIC's dollar bars have few spikes, suggesting modest or inconsistent capital flow.")
        st.write("- **ADA:** ADA's dollar bars show a general drop, implying capital might be flowing out or market participation is low.")
        st.write("- **ETH:** ETH's dollar bars show a slight upward trend with occasional spikes, reflecting moments of strong capital inflow amid stable trading.")
    
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        if bar_option == "Price Bars":
            ax.plot(df_price.index, df_price["Close"], label=f"Price Bars ({price_interval_label})")
            ax.set_title(f"Price Bars ({price_interval_label})")
            comment_title = "**Price Bars Comments:**"
            comments = [
                "- **MATIC:** MATIC's price bars are sparse with gaps, indicating intermittent trading, but the trend is upward.",
                "- **ADA:** ADA's 15-minute price bars are smooth and generally lower, perhaps due to steady sell pressure.",
                "- **ETH:** ETH's price bars are mostly continuous with one gap and high ups and downs, showing a bullish trend with rapid fluctuations."
            ]
        elif bar_option == "Tick Bars":
            ax.plot(df_tick.index, df_tick["Close"], label=f"Tick Bars (Every {tick_size} Trades)", color="orange")
            ax.set_title(f"Tick Bars (Every {tick_size} Trades)")
            comment_title = "**Tick Bars Comments:**"
            comments = [
                "- **ETH:** ETH's tick bars change quickly, showing high liquidity and fast bursts of trading.",
                "- **ADA:** ADA's tick bars are less frequent but have larger swings, likely due to lower liquidity.",
                "- **MATIC:** MATIC's tick bars steadily increase with mild changes, suggesting gradual investor interest."
            ]
        elif bar_option == "Volume Bars":
            ax.plot(df_volume.index, df_volume["Close"], label=f"Volume Bars (Every {volume_threshold} Volume)", color="green")
            ax.set_title(f"Volume Bars (Every {volume_threshold} Volume)")
            comment_title = "**Volume Bars Comments:**"
            comments = [
                "- **ETH:** ETH's volume bars are mostly flat with small jumps at a threshold of 10, meaning high trading frequency smooths changes.",
                "- **ADA:** ADA's volume bars show clear fluctuations at 10, indicating even modest volumes are significant due to lower liquidity.",
                "- **MATIC:** MATIC's volume bars have distinct spikes at 10, capturing sudden bursts of trading activity."
            ]
        elif bar_option == "Dollar Bars":
            ax.plot(df_dollar.index, df_dollar["Close"], label=f"Dollar Bars (Every {dollar_threshold} USDT)", color="red")
            ax.set_title(f"Dollar Bars (Every {dollar_threshold} USDT)")
            comment_title = "**Dollar Bars Comments (using 10000 USDT):**"
            comments = [
                "- **MATIC:** MATIC's dollar bars have few spikes, suggesting modest or inconsistent capital flow.",
                "- **ADA:** ADA's dollar bars show a general drop, implying capital outflow or low market participation.",
                "- **ETH:** ETH's dollar bars show a slight upward trend with occasional spikes, reflecting moments of strong capital inflow."
            ]
        ax.legend()
        st.pyplot(fig)
        
        st.write(comment_title)
        for c in comments:
            st.write(c)


