import pandas as pd
import streamlit as st
import plotly.express as px



st.set_page_config(
    page_title="Stock price prediction Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.markdown(""" 
<style>
.plot-container.plotly
{
    margin-left: 20px;    
}
.st-emotion-cache-gi0tri.e1nzilvr1
{
    margin-left: 20px;         
}
.st-emotion-cache-183lzff.exotz4b0
{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px
    
}
</style>
""", unsafe_allow_html=True)


df = pd.read_csv('ind_eursenti.csv', sep=',', header=0)
indices = pd.read_csv('indices1.csv', sep=',', header=0)
indices_european = pd.read_csv('indices2.csv', sep=',', header=0)

indices3_europe = pd.read_csv('indices3_europe.csv', sep=',', header=0)
indices3_India = pd.read_csv('indices3_india.csv', sep=',', header=0)
#st.dataframe(df)

st.title(":bar_chart: Stock Price Prediction Dashboard")

# Column 1: Dropdowns

col1, col2 = st.columns([1, 3])
with col1:
    st.header("User Selections")
    options = ['2020', '2021', '2022','2023']
    selected_option = st.selectbox('Select the year', options)
    which_market_options = ["indian","european"]
    selected_market = st.selectbox('Select the market', which_market_options)
    if selected_market == "indian":
        df1 = df[["textfile", "Indiansenti"]]
    elif selected_market == "european":
        df1 = df[["textfile", "Europeansenti"]]
    substring1 = selected_option[2::]
    substring1 = substring1 + ".txt"

    condition = df1['textfile'].str[-6:] == substring1
    filtered_rows = df1[condition]

    quarters = ['1st', '2nd', '3rd']
    selected_quarter = st.selectbox('Select a quarter', quarters)

    if selected_quarter == '1st':
        final_rows = filtered_rows.head(4)
    elif selected_quarter == '2nd':
        final_rows = filtered_rows.iloc[4:8]
    elif selected_quarter == '3rd':
        final_rows = filtered_rows.iloc[8:12]

    # Column 2: Bar chart
with col2:
    st.header("Sentiment Scores")
    st.text("This graph shows sentiment scores in different quarters in different years based on you selections.\nThe X-axis shows the month and the Y-axis shows shows the sentiment scores")
    x_values = final_rows['textfile'].str[0:3]
    print(x_values)
    sentimentsGraph = px.line(
        final_rows,
        x=x_values,
        y="Indiansenti" if selected_market == 'indian' else "Europeansenti",
        title="<b>Monthly sentiment scores</b>",
        color_discrete_sequence=['#1f77b4'],
        template="plotly_white",
    )
    sentimentsGraph.update_layout(
        xaxis_title='Month',  # Set x-axis label
        yaxis_title='Sentiment Score',  # Set y-axis label
    )       

    st.plotly_chart(sentimentsGraph, use_container_width=True)
    
#part2
col3, col4 = st.columns([3, 1])

with col4:
    st.header("User Selections")
    which_market_options = ["indian","european"]
    selected_option_market = st.selectbox('Select the market', which_market_options, key='market_selector_2')
    options = ['2020', '2021', '2022','2023']
    selected_option_year = st.selectbox('Select the year', options, key='year_selector_2')
    options_months = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
    ]
    selected_option_month = st.selectbox("select the month", options_months, key='month_selector_2')
    filtered_rows_2 = None
    if selected_option_market == "indian":
        substring3 = selected_option_month[0:3:]
        substring4 = selected_option_year[-2::]
        substring4 = substring4 + ".txt"

        condition_1 = indices['textfile'].str[:3] == substring3 
        filtered_rows_1 = indices[condition_1]

        condition_2 = filtered_rows_1['textfile'].str[-6:] == substring4
        filtered_rows_2_intermediate = filtered_rows_1[condition_2]
        filtered_rows_2 = filtered_rows_2_intermediate
    
    elif selected_option_market == "european":
        substring3 = selected_option_month[0:3:]
        substring4 = selected_option_year[-2::]
        substring4 = substring4 + ".txt"

        condition_1 = indices_european['textfile'].str[:3] == substring3 
        filtered_rows_1 = indices_european[condition_1]

        condition_2 = filtered_rows_1['textfile'].str[-6:] == substring4
        filtered_rows_2_intermediate = filtered_rows_1[condition_2]
        filtered_rows_2 = filtered_rows_2_intermediate

    # Your string representation of a dictionary
    series1 = filtered_rows_2['investor behavior']
    series_with_dicts = []
    market_mood = filtered_rows_2['market mood'].to_string(index=False)
    st.write("market mood: ",market_mood)

    for s in series1:
    # Convert each string representation of dictionary to an actual dictionary
        dict_representation = eval(s)  # Using eval() to evaluate the string literal

    # Print the resulting Series with dictionaries
    print(dict_representation.keys())
    print(dict_representation.values())
    

with col3:
    st.header("Investor Behavior")
    st.text("This graph shows how positive, negative and neutral investors are towards the market")
    colors = ['#2ca02c', '#ff4d4d', '#ffeb3b'] 
    
    fig = px.pie(values=dict_representation.values(), names=dict_representation.keys(), title='investor behavior distribution',
                color_discrete_sequence=colors)
    fig.update_layout(width=666, height=416)
    st.plotly_chart(fig)

indices2 = indices.copy()  # Make a copy to avoid modifying the original data
indices2 = indices2.drop(columns=['investor behavior'])

st.header("Yearly Market Mood")

year = []
for index, row in indices2.iterrows():
    var1 = row['textfile'][-6:]
    var1 = var1[0:2]
    var1= "20" + var1
    year.append(var1)

print(len(year))
indices2['year'] = year
st.text("This graph plots the market mood variations in the last few years for both Indian and European markets.\nThe X-axis represents the months and the Y-axis represents market mood values.\nEach line represents a different year.")

fig2 = px.line(indices2,
               x=['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']*4, y='market mood', color='year',
                   title = "Indian Stock Market Market Mood")
fig2.update_layout(
    xaxis_title='Month',  # Set x-axis label
    yaxis_title='Market Mood',  # Set y-axis label
)
st.plotly_chart(fig2)

#europe

indices_european2 = indices_european.copy()  # Make a copy to avoid modifying the original data
indices_european2 = indices_european2.drop(columns=['investor behavior'])

year_europe = []
for index, row in indices_european2.iterrows():
    var1 = row['textfile'][-6:]
    var1 = var1[0:2]
    var1= "20" + var1
    year_europe.append(var1)

print(len(year_europe))
indices_european2['year_europe'] = year_europe

fig3 = px.line(indices_european2,
               x=['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']*4, y='market mood', color='year_europe',
                   title = "European Stock Market Market Mood")
fig3.update_layout(
    xaxis_title='Month',  # Set x-axis label
    yaxis_title='Market Mood',  # Set y-axis label
)

st.plotly_chart(fig3)

#part3
col5, col6 = st.columns([1, 1])

with col5:
    st.header("Indian market Stats")
    st.write(f"###### Impact on Investor Confidence:   {indices3_India['Impact on Investor Confidence'].to_string(index=False)}")
    st.write("###### Impact on Market Stability:   " + indices3_India['Impact on Market Stability'].to_string(index=False))
    st.write("###### Impact on Economic Trends:   " + indices3_India['Impact on Economic Trends'].to_string(index=False))

with col6:
    st.header("European market Stats")
    st.write(f"###### Impact on Investor Confidence:   {indices3_europe['Impact on Investor Confidence'].to_string(index=False)}")
    st.write(f"###### Impact on Market Stability:   {indices3_europe['Impact on Market Stability'].to_string(index=False)}")
    st.write(f"###### Impact on Economic Trends:   {indices3_europe['Impact on Economic Trends'].to_string(index=False)}")


