import streamlit as st
import pandas as pd
import pickle
import time

st.set_page_config(
    page_title="Estimasi Hotel Yogyakarta",
    page_icon=":hotel:"
)

# Load Variable
hotelFacilities = pickle.load(
    open('Data/Variable/hotelFacilities.pkl', 'rb'))
roomFacilities = pickle.load(
    open('Data/Variable/roomFacilities.pkl', 'rb'))
nearestPoint = pickle.load(
    open('Data/Variable/pointInterests.pkl', 'rb'))
colOri = pickle.load(
    open('Data/Variable/col.pkl', 'rb'))

# Load Model
xgbModel = pickle.load(open('Model/xgbModel.pkl', 'rb'))
svrModel = pickle.load(open('Model/svrModel.pkl', 'rb'))
rfModel = pickle.load(open('Model/rfModel.pkl', 'rb'))

def user_input_features():
    starRating = st.sidebar.slider('Star Rating', 0, 5, 3)
    builtYear = st.sidebar.slider('Built Year', 1900, 2023, 1960)
    size = st.sidebar.slider('Room Size (m2)', 2.0,
                             100.0, 50.0, 0.1, format='%0.1f')
    occupancy = st.sidebar.slider('Occupancy', 1, 5, 3)
    childAge = st.sidebar.slider('Child Age', 0, 18, 9)
    childOccupancy = st.sidebar.slider('Child Occupancy', 0, 5, 2)
    breakfast = st.sidebar.checkbox('Breakfast Included')
    wifi = st.sidebar.checkbox('Wifi Included')
    refund = st.sidebar.checkbox('Free Cancellation / Refund')
    livingRoom = st.sidebar.checkbox('Living Room')
    hotelFacilitie = st.sidebar.multiselect(
        'Hotel Facilities', (hotelFacilities))
    roomFacilitie = st.sidebar.multiselect(
        'Room Facilities', (roomFacilities))
    pointInterest = st.sidebar.multiselect(
        'Point of Interest', (nearestPoint))

    # Handle Checkbox
    breakfast = 1 if breakfast else 0
    wifi = 1 if wifi else 0
    refund = 1 if refund else 0
    livingRoom = 1 if livingRoom else 0

    # Handle Multiselect
    hotelFacilitie = ','.join(hotelFacilitie)
    roomFacilitie = ','.join(roomFacilitie)
    pointInterest = ','.join(pointInterest)

    data = {
            'starRating': starRating,
            'builtYear': builtYear,
            'size': size,
            'baseOccupancy': occupancy,
            'maxChildAge': childAge,
            'maxChildOccupancy': childOccupancy,
            'isBreakfastIncluded': breakfast,
            'isWifiIncluded': wifi,
            'isRefundable': refund,
            'hasLivingRoom': livingRoom,
            'hotelFacilities': hotelFacilitie,
            'roomFacilities': roomFacilitie,
            'nearestPoint': pointInterest
            }
    features = pd.DataFrame(data, index=[0])
    return features

# create function to create dataframe with 0 and 1 value
def create_df(dfOri, df_name, df, prefix):
    value = prefix+dfOri[df_name][0]
    for i in range(0, len(df.columns)):
        column_name = df.columns[i]
        if column_name in value:
            df.loc[0, column_name] = 1
        else:
            df.loc[0, column_name] = 0
    return df

# Title
st.title('Yogyakarta Hotel Price Estimation')
st.write(
    'For more info about this project, please visit my [**Github**](https://github.com/Liore-S/hotel-yoyakarta)')

# Sidebar
st.sidebar.header('User Input Features')
df = user_input_features()

# Main Panel
st.header('User Input features')
st.write(df)

# create empty dataframe for hotelFacilities, roomFacilities, nearestPoint, with column name from hotelFacilities, roomFacilities, nearestPoint
roomFacilities_df = pd.DataFrame(columns=roomFacilities)
hotelFacilities_df = pd.DataFrame(columns=hotelFacilities)
nearestPoint_df = pd.DataFrame(columns=nearestPoint)

create_df(df, 'roomFacilities', roomFacilities_df, 'Room_')
create_df(df, 'hotelFacilities', hotelFacilities_df, 'Hotel_')
create_df(df, 'nearestPoint', nearestPoint_df, 'Point_')
# roomFacilities_df

df = df.drop(['hotelFacilities', 'roomFacilities', 'nearestPoint'], axis=1)
df = pd.concat([df, hotelFacilities_df, roomFacilities_df, nearestPoint_df], axis=1)

# change all column data type to unit8 except the first column
df = df.astype({col: 'float64' for col in df.columns[:2]})
df = df.astype({col: 'uint8' for col in df.columns[2:]})

# check df column order with model column order using colOri, if not the same print the worng column
colOri = colOri[1:]
if df.columns.tolist() == colOri.all():
    st.info("Column order is correct.")
else:
    mismatched_columns = [(idx, df_col, model_col) for idx, (df_col, model_col) in enumerate(zip(df.columns.tolist(), colOri)) if df_col != model_col]

    if len(mismatched_columns) > 0:
        st.warning("The order of the columns is not the same as the model. Mismatched columns:")
        for idx, df_col, model_col in mismatched_columns:
            st.write(f"At index {idx}: DataFrame column '{df_col}' - Model column '{model_col}'")

# Predict Button
st.write('Press button below to predict :')
model = st.selectbox('Select Model', ('XGBoost', 'Random Forest', 'SVR'))

if model == 'XGBoost' and st.button('Predict'):
    bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        status_text.text("%i%% Complete" % i)
        bar.progress(i)
        time.sleep(0.01)

    # Formatting the prediction
    prediction = xgbModel.predict(df)
    rfPrediction = rfModel.predict(df)
    svrModel = svrModel.predict(df)
    
    formaString = "Rp{:,.2f}"
    prediction = float(prediction[0])
    formatted_prediction = formaString.format(prediction)
    # prediction = rfModel.predict(df)
    time.sleep(0.08)

    # print the prediction
    st.subheader('Prediction')
    st.metric('Price (IDR)', formatted_prediction)

    # empty the progress bar and status text
    time.sleep(0.08)
    bar.empty()
    status_text.empty()
   
elif model == 'Random Forest' and st.button('Predict'):
    bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        status_text.text("%i%% Complete" % i)
        bar.progress(i)
        time.sleep(0.01)

    # Formatting the prediction
    prediction = rfModel.predict(df)
    
    formaString = "Rp{:,.2f}"
    prediction = float(prediction[0])
    formatted_prediction = formaString.format(prediction)
    time.sleep(0.08)

    # print the prediction
    st.subheader('Prediction')
    st.metric('Price (IDR)', formatted_prediction)

    # empty the progress bar and status text
    time.sleep(0.08)
    bar.empty()
    status_text.empty()
    
elif model == 'SVR' and st.button('Predict'):
    bar = st.progress(0)
    status_text = st.empty()
    for i in range(1, 101):
        status_text.text("%i%% Complete" % i)
        bar.progress(i)
        time.sleep(0.01)

    # Formatting the prediction
    prediction = svrModel.predict(df)
    
    formaString = "Rp{:,.2f}"
    prediction = float(prediction[0])
    formatted_prediction = formaString.format(prediction)
    # prediction = rfModel.predict(df)
    time.sleep(0.08)

    # print the prediction
    st.subheader('Prediction')
    st.metric('Price (IDR)', formatted_prediction)

    # empty the progress bar and status text
    time.sleep(0.08)
    bar.empty()
    status_text.empty()