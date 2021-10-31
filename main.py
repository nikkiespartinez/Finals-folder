from re import X
import pandas as pd
import streamlit as st

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash.dependencies import Input, Output

st.set_page_config(page_title='Electric Car Dashboard', layout='wide')

col1, col2 = st.columns(2)

header = st.container()
dataset = st.container()
news_data = st.container()
comparison_chart = st.container()
project_details = st.container()
fast_data = st.container()
battery_data = st.container()
footer = st.container()

st.markdown(
    """
    <style>
    .main {
        background-color:#1D1D1D;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with header:
    col1.title('A Closer Look Into Electric Cars')
    col1.text('A Python Project by Nikki Espartinez')

@st.cache
def get_data(filename):
    ev_data = pd.DataFrame.read_csv(filename)

    return ev_data

df = pd.read_csv('clean_data_latest.csv').head(50)

# Sidebar
with project_details:
    st.sidebar.header('Interactive Controls')
    st.sidebar.text('Please use the following \nfilters to interact with the \ngraphs on the right')
   
    # Multiselect
    car_select = st.sidebar.multiselect('Type of Car', options=df['Name'].unique(), default=df['Name'].head(10))
    slider_price = st.sidebar.slider('Select Price Range (USD)', max_value=300000, min_value=10000)
    st.sidebar.write('Selected Price:', slider_price, 'USD')
    drive_price = st.sidebar.selectbox('Select Type of Drive/Power:', options=df['Power'].unique())


    df_query = df.query('Name==@car_select & Price_USD<=@slider_price & Power==@drive_price')
    #df_slider1 = df.query('Price_USD==@slider_price')
    
    about = st.sidebar.button('About this project')
    if about:
        st.sidebar.text('This is a Python project \nby Nikki Espartinez. \nBuilt with Streamlit, \nPandas, Python 8 & Plotly. \nThank you General Assembly and \nCraig for the guidance.')
    # st.sidebar.text('Why? Because we want to be a \nlot more informed with this \nemerging innovation in the \nautomobile/transportation industry \nthrough data.')
    # st.sidebar.header('About the Maker')
    # st.sidebar.text('Nikki Espartinez is a Designer, \nWriter & a Qualitative User \nResearcher. This is her first time \ntaking up a bootcamp in \nPython Programming. \nThe experience has been fulfilling, \nchallenging and humbling.')

# Table of news data
with news_data:
    col2.header('EV In the News')
    col2.text('What the world is saying about the EV revolution...')
    #st.text('Top headlines from newsapi.org')
    
    ev_data = pd.read_csv('headlines_ev.csv')
    #st.write(ev_data.head(5), index=True)

    agree = col2.checkbox('Show News Data')
    if agree:
        source = col2.multiselect('To view Top News, select the source name below:', options=ev_data['Source'].unique())
        df_selection = ev_data.query('Source==@source')
        col2.dataframe(df_selection)
        #col1.expander("More Information")
        col2.text("These are news articles gathered from the open-source API site called newsapi.org. \nData was cleaned, published October 2021.")

    #news_data = get_data('headlines_ev.csv')

    # fig = go.Figure(data=go.Table(header=dict(values=list(df[['Title', 'Source', 'URL']].columns),
    #                                      fill_color='#eeeeee',
    #                                      align='left'), cells=dict(values=[df.Title, df.Source, df.URL],
    #                                                               fill_color='#FCFCFC',
    #                                                               align='left')))
    # fig.update_layout(
    # height=800,
    # showlegend=False,
    # )
    
    # fig.show()

with comparison_chart:
    col1.header('The Price Of Turning Electric')
    col1.text('Tesla and Porsche remains the top tier brands, price-wise.')

    most_exp = df.Price_USD.max()

    #most_exp_format = "${:,2f}".format(most_exp)
    #name_exp = df.get('Name' in most_exp)
    col1.metric('Most Expensive:', most_exp, 'Porsche Taycan Turbo S')
    #col1.metric('Least Expensive:', '90000', 'Tesla')

    #fig2 = px.line(df, x='Name', y='Price_USD', title='Price of cars comparison',
        #labels={'Price_USD': 'Price in USD'})

    #max_depth = col2.slider('Explore the range of prices', min_value=10, max_value=300000, value=50000, step=10)

    #n_seats = pd.DataFrame(df['NumberofSeats']).value_counts()
    #st.selectbox(n_seats, options=['1-5', '6-10', '11-15', '16-above'], index=0)

    #n_estimators = sel_col.selectbox('Pick any number of seats', options=['1-5', '6-10', '11-15', '16-above'], index=0)

    # This is the Bar Graph

    fig2 = px.bar(df_query, x='Name', y='Price_USD', title='Price of cars comparison',
        labels={'Price_USD': 'Price in USD',
        'Battery_clean': 'Strength of Battery (KWH)'},
        hover_data=['Top Speed (KM/H)'], color='Battery_clean')

    fig2.update_traces(marker_color='#208BB9', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
    fig2.update_layout(paper_bgcolor = '#1D1D1D', yaxis=dict(gridcolor='#3E3E3E'), xaxis_tickangle=-45)

    col1.write(fig2)


with fast_data:
    col1.header('How Fast Are These EV Cars Nowadays?')
    col1.text('Modern day electric vehicles have come a long way.')

    fastest = df['Speed New'].max()
    col1.metric('Fastest Car:', fastest, 'Porsche Taycan Turbo S')

    df = pd.read_csv('clean_data_latest.csv')


    fig3 = px.scatter(df_query, x='Speed New', y='Name', title='A Comparison', size='Price_USD', color='Range (ml)',
                  labels={'Speed New': 'Speed (MPH)',
                         'Price_USD': 'Price in USD',
                         'Range (ml)': 'Car Range'})

    fig3.update_layout(paper_bgcolor = '#1D1D1D', yaxis=dict(gridcolor='#3E3E3E'), xaxis=dict(gridcolor='#3E3E3E') )

    col1.write(fig3)

    # min_range = 10
    # max_range = 1000
    
    # @app.callback(Output('Range (ml)','figure'),Input('slider','value'))
    # def build_chart_by_range(min_range, max_range):
    #     filtered_data = df[(df['Range (ml)']>=min_range)&(df['Range (ml)']<=max_range)]
    #     fig1 = px.scatter(df, x='Speed New', y='Name', title='A Comparison', size='Price_USD', color='Battery_clean',
    #             labels={'Speed New': 'Speed (MPH)',
    #                     'Price_USD': 'Price in USD',
    #                     'Battery_clean': 'Strength of Battery (KWH)'})
    #     return fig1
    
    
   
   #st.write(fig1)
    #x = st.slider('Select Car Range', max_value=1000)
    #st.write('Car Range:', x)

with battery_data:
    col1.header('Battery Life: An Analysis')
    col1.text('Which ones have the most powerful batteries?')

    fig4 = px.bar(df_query, x='Power', y='Battery_clean', color='Name', labels={'Battery_clean': 'Strength of Battery (KWH)',
                         'Power': 'Type of Drive/Power'})

    fig4.update_layout(barmode='group', xaxis_tickangle=-45, yaxis=dict(gridcolor='#3E3E3E'))

    col1.write(fig4)

with footer:
    st.text('Data from newsapi.org, https://www.kaggle.com/kkhandekar/cheapest-electric-cars \nAdditional tutorials from: Youtube (@Coding is fun, @Misra Turp). \nEV Data Analysis by Nikki Espartinez, 2021©')
