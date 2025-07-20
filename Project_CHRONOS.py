import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objects as go


# CSS for styling the dashboard
st.markdown(
    """
    <style>
    /* Streamlit's built-in dark theme will handle the main background color */

    /* General text and element sizing */
    html, body {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; /* Modern font st*/
        font-size: 20px; /* Base font size for overall larger text */
    }

    /* Headings (colors compatible with dark theme) */
    h1 {
        color: #f0f2f6 !important; /* Ensure headings are light */
        font-size: 3.5em !important; /* Larger H1 */
        text-align: center;
        margin-bottom: 0.5em; /* Spacing below headings */
    }
    h2 {
        color: #f0f2f6 !important;
        font-size: 2.5em !important; /* Larger H2 */
        text-align: center;
        margin-top: 1.5em; /* Spacing above headings */
        margin-bottom: 0.8em;
    }
    h3 {
        color: #f0f2f6 !important;
        font-size: 2em !important; /* Larger H3 */
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }
    h4, h5, h6 {
        color: #f0f2f6 !important;
    }
    p {
        color: #f0f2f6 !important;
        font-size: 1.2em; /* Paragraph text size (24px) */
        line-height: 1.6; /* Better line spacing */
    }

    /* Streamlit widgets specific styling */
    .stTextInput label, .stRadio > div > label > div > span, .stSelectbox label, .stDateInput label {
        color: #f0f2f6 !important; /* Labels for inputs (light color) */
        font-size: 1.2em; /* Matches new paragraph text size */
    }
    .stTextInput input, .stSelectbox > div > div, .stDateInput input {
        background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent input fields */
        color: #f0f2f6; /* Input text color back to light for dark theme */
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 5px;
        padding: 0.5em 1em;
        font-size: 1.1em; /* Input text size, slightly smaller than label */
    }
    .stTextInput input:focus, .stSelectbox > div > div:focus, .stDateInput input:focus {
        border-color: #4CAF50; /* Green highlight on focus */
        box-shadow: 0 0 0 0.1rem #4CAF50;
    }

    /* Streamlit metric values and labels (colors compatible with dark theme) */
    div[data-testid="stMetricValue"] {
        color: #f0f2f6 !important;
        font-size: 1.8em !important; /* Significantly larger metric values (36px) */
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #d0d2d6 !important; /* Slightly dimmer label for contrast */
        font-size: 1em !important; /* Matches base font size (20px) */
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1.2em !important; /* Larger delta values */
    }

    /* Style for the dataframe in "Today's Data" (colors compatible with dark theme) */
    .stDataFrame {
        background-color: #3C445C !important; /* Solid dark blue-grey background for the table */
        color: #f0f2f6 !important;
        font-size: 1.2em; /* Larger dataframe text (24px) */
        border-radius: 8px; /* Slightly rounded corners */
        overflow: hidden; /* Ensures borders are contained */
    }
    .stDataFrame thead th {
        color: #f0f2f6 !important;
        background-color: #4A536F !important; /* Lighter blue-grey for table header */
        font-size: 1.2em; /* Larger dataframe header text (24px) */
        font-weight: bold;
    }
    .stDataFrame tbody tr {
        color: #f0f2f6 !important;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #424A64 !important; /* Slightly lighter shade for odd rows */
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #384055 !important; /* Slightly darker shade for even rows */
    }

    /* Custom styles for timeframe "buttons" (colors compatible with dark theme) */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.15); /* More visible transparent background */
        color: #f0f2f6; /* Light text */
        border: 1px solid rgba(255, 255, 255, 0.4); /* Clearer border */
        border-radius: 5px;
        padding: 8px 15px;
        margin: 5px;
        font-size: 1.2em; /* Larger button text (24px) */
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        min-width: 80px; /* Ensure buttons have consistent width */
        text-align: center;
        display: inline-flex; /* Use flex to center content */
        align-items: center;
        justify-content: center;
    }
    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.3); /* More opaque on hover */
        border-color: #4CAF50; /* Green border on hover */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the page configuration for wide layout
st.set_page_config(layout="wide")

#custom buttons
if 'selected_time_range' not in st.session_state:
    st.session_state.selected_time_range = "1D" # Default selection


st.markdown("<h1 style='text-align: center;'>Project: CHRONOS - Stock Dashboard</h1>", unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center;'>Charting Historical Returns Online, Now Or Soon!</h2>", unsafe_allow_html=True)

st.header("Stock Selection & Period")

# Ticker Symbol Input
ticker_symbol = st.text_input("Enter Stock Ticker ", "AAPL").upper()

# Fixed Time Set Selection 
period_options = {
    "1D": {"period": "1d", "interval": "5m"},#5 minute intervals
    "5D": {"period": "5d", "interval": "30m"},#30 minute interval
    "1W": {"period": "7d", "interval": "1d"}, # 7 days daily candles
    "1M": {"period": "1mo", "interval": "1d"},#day
    "1Y": {"period": "1y", "interval": "1wk"},#week
    "5Y": {"period": "5y", "interval": "1wk"},#week
    "MAX": {"period": "max", "interval": "1mo"} # Max available data, monthly interval
}

# Custom Time Range Buttons
st.write("Select Time Range:")
cols = st.columns(len(period_options))
for i, (label, params) in enumerate(period_options.items()):
    with cols[i]:
        if st.session_state.selected_time_range == label:
            # for designing a  selected button
            st.markdown(
                f"""
                <div class="stButton" style="width: auto;">
                    <button class="selected" style="background-color: #4CAF50; border-color: #4CAF50; color: white; font-weight: bold;">
                        {label}
                    </button>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Render a normal st.button that updates state on click
            if st.button(label, key=f"time_btn_{label}"):
                st.session_state.selected_time_range = label
                st.rerun()

# Get selected period params from session state
selected_period_params = period_options[st.session_state.selected_time_range]
selected_yf_period = selected_period_params["period"]
selected_yf_interval = selected_period_params["interval"] # Corrected line

# --- Data Fetching Logic (Cached) ---
#cache needed
@st.cache_data(ttl=3600)
def get_stock_data(ticker, period=None, interval=None, start=None, end=None):
    try:
        if period and interval:
            stock_data = yf.download(ticker, period=period, interval=interval)
        elif start and end:
            stock_data = yf.download(ticker, start=start, end=end)
        else:
            return None

        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.droplevel(level=1)
        
        if stock_data.empty:
            return None
        
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            stock_data[col] = pd.to_numeric(stock_data[col], errors='coerce')
        stock_data.dropna(subset=['Close'], inplace=True)
        
        return stock_data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}. Please check the ticker symbol or your internet connection.")
        return None

# Fetch data for main chart based on selected period
main_stock_data = get_stock_data(ticker_symbol, period=selected_yf_period, interval=selected_yf_interval)

# Get Ticker object for company info and news
@st.cache_resource
def get_ticker_object(ticker):
    return yf.Ticker(ticker)

company_ticker_obj = get_ticker_object(ticker_symbol)

# --- Display Main Dashboard Content (only if data is successfully fetched for main ticker) ---
if main_stock_data is not None and not main_stock_data.empty:
    st.subheader(f"Displaying data for {ticker_symbol} ({st.session_state.selected_time_range} - {selected_yf_interval} interval)")

    # --- Candlestick Chart ---
    st.subheader("Candlestick Chart")
    
    fig = go.Figure(data=[go.Candlestick(x=main_stock_data.index,
                                        open=main_stock_data['Open'],
                                        high=main_stock_data['High'],
                                        low=main_stock_data['Low'],
                                        close=main_stock_data['Close'],
                                        increasing_line_color='green',
                                        decreasing_line_color='red')])

    fig.update_layout(
                      xaxis_rangeslider_visible=False,
                      title_text=f'{ticker_symbol} Candlestick Chart',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      height=850,
                      paper_bgcolor='black',
                      plot_bgcolor='black'
                     )
    st.plotly_chart(fig, use_container_width=True)

    # --- Key Metrics ---
    st.markdown("<h2 style='text-align: center;'>Key Metrics</h2>", unsafe_allow_html=True)

    if len(main_stock_data) >= 2:
        latest_close = main_stock_data['Close'].iloc[-1].item()
        previous_close = main_stock_data['Close'].iloc[-2].item()
        daily_change = latest_close - previous_close
        daily_change_percent = (daily_change / previous_close) * 100
        latest_volume = main_stock_data['Volume'].iloc[-1].item()

        period_avg = main_stock_data['Close'].mean().item()
        returns_for_period = ((main_stock_data['Close'].iloc[-1].item() - main_stock_data['Close'].iloc[0].item()) / main_stock_data['Close'].iloc[0].item()) * 100

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(label=f"Latest Close ({ticker_symbol})", value=f"${latest_close:.2f}")

        with col2:
            delta_color_val = "normal" if daily_change >= 0 else "inverse"
            st.metric(
                label="Daily Change",
                value=f"${daily_change:.2f}",
                delta=f"{daily_change_percent:.2f}%",
                delta_color=delta_color_val
            )

        with col3:
            st.metric(label="Volume", value=f"{latest_volume:,.0f}")
        
        with col4:
            st.metric(label="Period Avg. Close", value=f"${period_avg:.2f}")
        
        with col5:
            returns_delta_color_val = "normal" if returns_for_period >= 0 else "inverse"
            st.metric(
                label="Returns for Period",
                value=f"{returns_for_period:.2f}%",
                delta_color=returns_delta_color_val
            )

        # --- Today's Price Data (compact) ---
        st.markdown("---")
        st.subheader(f"Today's {ticker_symbol} Data (Last Available)")
        if not main_stock_data.empty:
            today_data = main_stock_data.iloc[-1]
            today_df = pd.DataFrame({
                "Metric": ["Date", "Open", "High", "Low", "Close", "Volume"],
                "Value": [
                    today_data.name.strftime('%Y-%m-%d %H:%M:%S'),
                    f"${today_data['Open']:.2f}",
                    f"${today_data['High']:.2f}",
                    f"${today_data['Low']:.2f}",
                    f"${today_data['Close']:.2f}",
                    f"{today_data['Volume']:,.0f}"
                ]
            })
            st.dataframe(today_df.set_index("Metric"), use_container_width=True)
        else:
            st.info("No intraday data available for today.")

    else:
        st.warning("Not enough data points to calculate daily change and display full metrics for the selected period. Try a longer period.")

    st.info(f"Data last updated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.error(f"Could not fetch data for {ticker_symbol} for the selected period. Please check the ticker symbol or try a different time range.")

# --- Returns Section ---
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>Price Performance (Returns)</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def calculate_period_return(ticker, days=None, months=None, years=None, ytd=False):
    today = dt.date.today()
    start_date = None
    
    if ytd:
        start_date = dt.date(today.year, 1, 1)
    elif days:
        start_date = today - dt.timedelta(days=days)
    elif months:
        start_date = today - dt.timedelta(days=months * 30)
    elif years:
        start_date = today - dt.timedelta(days=years * 365)
    
    if not start_date or start_date >= today:
        return None, "N/A"

    data = get_stock_data(ticker, start=start_date, end=today)
    
    if data is not None and not data.empty and len(data) >= 2:
        first_price = data['Close'].iloc[0].item()
        last_price = data['Close'].iloc[-1].item()
        if first_price == 0: return None, "N/A"
        percent_return = ((last_price - first_price) / first_price) * 100
        return percent_return, "valid"
    return None, "N/A"

returns_data = {
    "1 Week": calculate_period_return(ticker_symbol, days=7),
    "1 Month": calculate_period_return(ticker_symbol, months=1),
    "3 Months": calculate_period_return(ticker_symbol, months=3),
    "YTD": calculate_period_return(ticker_symbol, ytd=True),
    "1 Year": calculate_period_return(ticker_symbol, years=1),
    "3 Years": calculate_period_return(ticker_symbol, years=3)
}

for label, (value, status) in returns_data.items():
    if status == "valid":
        delta_color_val = "normal" if value >= 0 else "inverse"
        col_label, col_value = st.columns([0.4, 0.6])
        with col_label:
            st.write(f"**{label}**")
        with col_value:
            st.metric(label="", value=f"{value:.2f}%", delta_color=delta_color_val)
    else:
        col_label, col_value = st.columns([0.4, 0.6])
        with col_label:
            st.write(f"**{label}**")
        with col_value:
            st.write("N/A")

# --- About the Company Section ---
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>About the Company</h2>", unsafe_allow_html=True)

company_info = company_ticker_obj.info
if company_info:
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {company_info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {company_info.get('sector', 'N/A')}")
    
    with col2:
        st.write(f"**Industry:** {company_info.get('industry', 'N/A')}")
        st.write(f"**CEO:** {company_info.get('ceo', 'N/A')}")
    
    website_url = company_info.get('website', '#')
    website_display = website_url if website_url != '#' else 'N/A'
    st.write(f"**Website:** <a href='{website_url}' target='_blank'>{website_display}</a>", unsafe_allow_html=True)

    summary = company_info.get('longBusinessSummary', 'No business summary available.')
    summary_sentences = summary.split('.')
    display_summary = ". ".join(summary_sentences[:3]) + ("." if len(summary_sentences) > 3 else "")
    
    st.write(f"**Business Summary:** {display_summary}")
else:
    st.info(f"Could not fetch company information for {ticker_symbol}.")
