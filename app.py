import streamlit as st

# -- Set page config
apptitle = 'TDI Milestone'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# -- Default detector list
detectorlist = ['H1','L1', 'V1']

# Title the app
st.title('TDI Milestone by Abbas Booshehrian')

st.markdown("""
 * An interactive chart of stock closing prices using Streamlit and Plot.ly.
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

st.sidebar.markdown("## Select plot parameters:")
tick = st.sidebar.text_input('Ticker (e.g. AAPL):')
yr = st.sidebar.selectbox(
        "Year:", list(range(2010,2021)))
mon = st.sidebar.selectbox(
        "Month:", list(range(1,13)))

# st.title('Hello world')

# with st.echo():
#     x = 15

# with st.echo():
#     y = 50

# with st.echo():
#     z = x + y
#     st.write(z)

# ----------------CODE--------------
# import libraries
import pandas as pd
import streamlit as st
import plotly
from dotenv import load_dotenv
import requests

def closeGen(tick,yr,mon):
    pre = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
    interval = '60min'
    apiKey = tick
    url = pre + tick + '&interval=' + interval + '&apikey=' + apiKey + '&outputsize=full'

    r = requests.get(url)
    data_dict = r.json()

    data_items = data_dict.items()
    data_list = list(data_items)

    data = pd.DataFrame(data_list)

    df = pd.DataFrame.from_dict(data[1][1], orient='index')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'timestamp'})
    
    df['timestamp'] = pd.to_datetime(df['timestamp']) 
    df['1. open']= df['1. open'].astype(float)
    df['2. high']= df['2. high'].astype(float)
    df['3. low']= df['3. low'].astype(float)
    df['4. close']= df['4. close'].astype(float)
    df['5. volume']= df['5. volume'].astype(float)

    df['Year'] = df.timestamp.apply(lambda x: x.year)
    df['Month'] = df.timestamp.apply(lambda x: x.month)

    df_select = df[(df['Year'] == yr) & (df['Month'] == mon)]

    # Using plotly.express
    import plotly.express as px
    # dt = px.data.stocks()
    fig = px.line(df_select, x='timestamp', y='4. close')
    # Edit the layout
    fig.update_layout(title=tick+':'+str(mon)+'/'+str(yr),
                       xaxis_title='Time',
                       yaxis_title='Close Price')
    # fig.show()
    return fig

fig = closeGen(tick,yr,mon)
# st.pyplot(fig, clear_figure=True)
st.write(fig)