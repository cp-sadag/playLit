import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import autoML

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                 'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

#@st.cache
#def load_data(nrows):
    #data = pd.read_csv(DATA_URL, nrows=nrows)
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    #return data

#@st.cache
def load_data(uploadFileName):
    if uploadFileName is not None:
        try:
            #bytes_data = uploadFileName.read()
            #st.write("filename:", uploadFileName.name)
            #st.write(bytes_data)
            #data = uploadFileName.read()
            data = pd.read_csv(uploadFileName)
            #df = pd.DataFrame(data)
            return data
        except UnicodeDecodeError as e:
            st.error(f"error loading log.las: {e}")
    return None

st.title('The Data App')
# Sidebar Options & File Uplaod
st.sidebar.title('Data Explorer')
st.sidebar.write('Load data using file browser or specify full path to file to use the app.')
st.sidebar.write('c:\\user\\Downloads\\abc.csv or https://raw.githubusercontent.com/selva86/datasets/master/Cars93_miss.csv')
#if st.sidebar.checkbox('WSL'):
    #st.write(uploadFileName)
    #uploadFileName = uploadFileName[0].lower() + uploadFileName[1:]
    #uploadFileName = "/" + uploadFileName.replace(":", "/").replace("\\","/")

dataLoadStatus = st.sidebar.text('')
dataDescription = st.text('')
dataFrame = st.dataframe(None)
dataFrameDesc = st.dataframe(None)
#loadedData = st.dataframe(None)
uploadFileName = st.sidebar.text_input('Input File Name')
if uploadFileName is not None and len(uploadFileName) > 0:
    dataLoadStatus.text('Loading data...')
    data = pd.read_csv(uploadFileName)
    if data is not None:
        dataFrame.dataframe(data)
        dataFrameDesc.dataframe(pd.DataFrame(data.describe(include = "all")))
        dataLoadStatus.text('Loading data...done!')

uploadFile = st.sidebar.file_uploader('Load csv files') #, type=['.las'])
if uploadFile is not None:
    dataLoadStatus.text('Loading data...')
    data = pd.read_csv(BytesIO(uploadFile.getvalue()), sep=",")
    if data is not None:
        dataFrame.dataframe(data)
        dataFrameDesc.dataframe(pd.DataFrame(data.describe(include = "all")))
        dataLoadStatus.text('Loading data...done!')

#df = load_data(uploadFile)
#if df is not None:
    #st.sidebar.success('File Uploaded Successfully')
    #df

# Create a text element and let the reader know the data is loading.
# Load 10,000 rows of data into the dataframe.
#data = load_data(10000)
# Notify the reader that the data was successfully loaded.

#if st.checkbox('Show raw data'):
    #st.subheader('Raw data')
    #st.write(data)

    #st.subheader('Number of pickups by hour')
    #hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    #st.bar_chart(hist_values)

    ## Some number in the range 0-23
    #hour_to_filter = st.slider('hour', 0, 23, 17)
    #filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    #st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    #st.map(filtered_data)

option = st.sidebar.selectbox(
    "Select Data Upload Option",
   ("Preview", "Exploratory Analysis", "Engineering", "AutoML", "Visualization")
   )

if option=='Visualization':
    #st.plotly_chart(data, x=data[data.columns[2]],y=data[data.columns[2]])
    fig, ax = plt.subplots()
    ax.hist(data, bins=20)
    st.pyplot(fig)
    #HtmlFile = open("test.html", 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 
    #components.html(source_code, height = 900,width=900)

if option=='AutoML':
    #data = pd.read_csv("datasets/googleplaystore.csv")
    #st.write(data[data.columns[0:-1]])
    #st.write(data[data.columns[-1]])
    st.write(autoML.runAutoML(data[data.columns[0:-1]], data[data.columns[-1]]))
    X_train, X_test, y_train, y_test = autoML.setData(data[data.columns[0:-1]], data[data.columns[-1]])
    automl = autoML.autoMLSearch(X_train, y_train)
    st.write(automl.search())
    st.write(automl.rankings)
    st.write(autoML.bestPipeline(X_train, y_train, X_test, automl))

#df = pd.DataFrame({
      #'first column': [1, 2, 3, 4],
        #'second column': [10, 20, 30, 40]
        #})

#df = pd.read_csv("datasets/googleplaystore.csv")
#df
#chartData = pd.DataFrame(df[['Category', 'Rating']].groupby(['Category']))
#st.line_chart(chartData)
#chartData


#df = pd.read_csv("datasets/googleplaystore_user_reviews.csv")
#df
#st.line_chart(df)

#df = pd.read_csv("datasets/movies.csv")
#df
#st.line_chart(df)
