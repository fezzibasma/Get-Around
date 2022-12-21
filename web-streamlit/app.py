import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


### Config
st.set_page_config(
    page_title="GetAround Analysis",
    page_icon="🚗 ",
    layout="wide"
)

#DATA_URL = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
### App
st.title("GetAround Dashboard Analysis")

st.image("https://lever-client-logos.s3.amazonaws.com/2bd4cdf9-37f2-497f-9096-c2793296a75f-1568844229943.png")

st.markdown("""
    Hello there ! 👋
    Do you wanna know more about Getaround app ! You are in the perfect place ! 
    When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

    Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
    Compare fuel levels.
    Measure how many kilometers were driven.
    The checkin and checkout of our rentals can be done with three distinct flows:

    📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
      Connect: the driver doesn’t meet the owner and opens the car with his smartphone
    📝 Paper contract (negligible)
    By examining historical data gathered on the GetAround app we will try to answer these questions : 
    * threshold: how long should the minimum delay be?
    * scope: should we enable the feature for all cars? only Connect cars?
""")

st.caption('a caption')

st.markdown("---")


# Use `st.cache` when loading data is extremely useful
# because it will cache your data so that your app
# won't have to reload it each time you refresh your app

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv("prep/get_around_delay_analysis.csv",sep=";")
    return data

st.text('Load data ...')

data_load_state = st.text('Loading data ...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.header('Raw data')
    st.write(data)

data['delay']=data["delay_at_checkout_in_minutes"].apply(lambda x: 1 if x>10 
                                                                    else 0)

st.header('Dataset overview and first impressions')

st.markdown("Out first impression is that the delay is not the main reason to cancel the reservation.")

fig1 = px.pie(data, values='delay', 
    names='state', 
    title='Impact of the delay on the reservation, can the reservation be cancelled or not?',
    color_discrete_sequence=[ "#AA336A", "darkcyan"])

st.markdown("What about checkin type, time delta with previous rental in minutes, is there a relation? should we enable the feature for all cars? or only Connect cars?")

fig2 = px.histogram(data[data["time_delta_with_previous_rental_in_minutes"]>0.0], x="time_delta_with_previous_rental_in_minutes", color="checkin_type",
    labels={"value":'time_delta_with_previous_rental_in_minutes'},
    title='Frequency of car rent by agreement :',
    color_discrete_sequence=[ "#AA336A", "darkcyan"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Impact of the delay on the reservation, can the reservation be cancelled or not?")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
   st.subheader("Frequency of car rent by agreement")
   st.plotly_chart(fig2, use_container_width=True)

st.markdown("Here, we can see that owners prefer Mobile rental agreement because they are more frequent rather than Connect.")
st.subheader("Maybe is it more secure to meet the driver with Mobile agreement or are the Mobile agreement more frequent?")

fig3 = px.pie(data, values="time_delta_with_previous_rental_in_minutes",
     names='checkin_type',
     color_discrete_sequence=[ "#AA336A", "darkcyan"])

st.plotly_chart(fig3, use_container_width=True)

st.markdown("Here , we see that Mobile are more are more frequent rather than Connect. We have only 45% of Connect !")
st.markdown("Alright , you are maybe wondering... ")
st.subheader("How does delay impact check-out timing and which agreement has more impact in the check-out delay?")

fig4 = px.histogram(data_frame=data[data["time_delta_with_previous_rental_in_minutes"]>0.0], x='delay_at_checkout_in_minutes', color='checkin_type', histnorm='percent', 
    barmode='overlay',range_x=(-400,400),labels={"value":'Delay at checkout per minute'},
    title='How does delay impact check-out timing? :',
    color_discrete_sequence=[ "#AA336A", "darkcyan"])

st.markdown("Well, there is no surprise, the Mobile agreement will be slower than the Connect agreement, so the check-out delay will be higher")

st.plotly_chart(fig4, use_container_width=True)

st.markdown("")


st.header('How long should the minimum delay be ?')

data = data.dropna(subset=["time_delta_with_previous_rental_in_minutes", "delay_at_checkout_in_minutes"])
data_test = pd.melt(data, id_vars=['car_id', 'rental_id', 'state', 'checkin_type'], value_vars=['time_delta_with_previous_rental_in_minutes', 'delay_at_checkout_in_minutes'])

st.metric(label="car fleet", value=data_test['car_id'].nunique())


fig6 = px.ecdf(
    data_test[data_test['checkin_type']=='mobile'],
    x='value',
    color='variable',
    ecdfnorm= 'percent',
    range_x=(0, 600),
    color_discrete_sequence=[ "#AA336A", "darkcyan"],
    labels={"value":'threshold (minutes)', "percent":'proportion of users (%)'}
    )

fig7 = px.ecdf(
    data_test[data_test['checkin_type']=='connect'],
    x='value',
    color='variable',
    ecdfnorm= 'percent',
    range_x=(0, 600),
    color_discrete_sequence=[ "#AA336A", "darkcyan"],
    labels={"value":'threshold (minutes)', "percent":'proportion of users (%)'}
    )
    ##labels={"delay_at_checkout_in_minutes":'threshold (minutes)', "time_delta_with_previous_rental_in_minutes":'threshold (minutes)'}

##fig4 = px.ecdf(
##    data,
##    x="time_delta_with_previous_rental_in_minutes",
##    color="checkin_type",
##    ecdfnorm= 'percent',
##    range_x=[0, 800],
##    labels={"time_delta_with_previous_rental_in_minutes":'threshold (minutes)'}
##    )

##st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mobile")
    st.plotly_chart(fig6, use_container_width=True)

with col2:
   st.subheader("Connect")
   st.plotly_chart(fig7, use_container_width=True)

st.markdown("These plots are Cumulative Distribution Function (ECDF), it allow us to show the percentage of users impacted by the introduction of a threshold for minimum time delay")
st.markdown("We note that 48% of the population return their car on time with the mobile version, while 66% for the connect version. The minimum delay threshold for both versions is 30 minutes."
            "The return delay impacts the pick-up time in a proportional way and accumulates gradually over the day."
            "It would be possible to reduce the minimum threshold to 20 minutes for the connect version. We are missing one information here : the number of cancelations avoided by the owner due to the augmentation of the threshold.")
st.markdown("The threshold sould be lower for connect cars because there is much less late return.")
