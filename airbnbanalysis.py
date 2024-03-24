import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore data","Contact"],
                        icons=["house", "bar-chart-line","envelope"],
                        menu_icon="menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px",
                                                "---hover-color": "#212223"},
                                "nav-link-selected": {"background-color": "#0C86C8"}})
    
                                                    
df = pd.read_csv(r"C:\\Users\\elava\\Downloads\\Airbnb_Analysis-main\\Airbnb_Analysis-main\\airbnbdata1.csv",encoding='ISO-8859-1')

if selected == 'Home':
    st.markdown("# :chart_with_upwards_trend: :blue[Airbnb Analysis]")
    st.markdown(
        "#### :rainbow[Technologies used :]  Python Scripting, Mongodb, Data Preprocessing ,Visualization,EDA, Streamlit, MongoDb, PowerBI or Tableau.")
    st.markdown(
        "#### :rainbow[Domain :] Travel Industry, Property Management and Tourism.")
    st.write()
    st.markdown(
         "#### Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")


# OVERVIEW PAGE
if selected == "Explore data":
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.country.unique()),sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.sidebar.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='large')
    
    with col1:
        st.markdown("### :rainbow[Average Price for Room type]")
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                    )
        st.plotly_chart(fig,use_container_width=True)


        st.markdown("### :rainbow[Availability Analysis]")
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                    )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("### :rainbow[host response based on country]")
        fig = px.scatter(df.query(query),
                    x='host_name',
                    y='host_response_time',
                    color='country_code', 
                    hover_name='name')
        fig.update_geos(projection_type='orthographic')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.markdown("### :rainbow[Average Price in Country]")
        country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        st.markdown("### :rainbow[Availability in Country wise]")
        country_df = df.query(query).groupby('country',as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'availability_365', 
                                       hover_data=['availability_365'],
                                       locationmode='country names',
                                       size='availability_365',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("### :rainbow[ratings based on country and price]")
        fig = px.scatter(df.query(query),
                    x='country',
                    y='price',
                    color='average_rating', 
                    hover_name='name')
        fig.update_geos(projection_type='orthographic')
        st.plotly_chart(fig,use_container_width=True)


    st.markdown("### :rainbow[host response based on Country]")
    fig = px.scatter(df.query(query),
                x='host_name',
                y='host_response_time',
                color='country', 
                hover_name='name')
    fig.update_geos(projection_type='orthographic')
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### :rainbow[beds and bedrooms availability]")
    fig = px.pie(df.query(query), values='beds',
                         names='street',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['bedrooms'],
                         labels={'bedrooms': 'bedrooms'})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Airbnb Analysis in Map view")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df)
                

if selected == "Contact":
    st.markdown("### :violet[About Airbnb analysis] ")
    st.write("")
    st.markdown("####  This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")            
    st.write("")
    st.write("**:rainbow[My GitHub link]** ⬇️")
    #st.write("https://github.com/NivethaShanmugam01")
    st.write("**:rainbow[My linkedin link]** ⬇️")
    #st.write("www.linkedin.com/in/nivetha-shanmugam-81532a278/")

        