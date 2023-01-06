import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

import seaborn as sns
sns.set_theme(style="whitegrid")

load_dotenv(override=True)
from prophet import Prophet

def predict_prophet():
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Create an engine instance
    alchemyEngine = create_engine(SQLALCHEMY_DATABASE_URI)
    # Connect to PostgreSQL server

    dbConnection = alchemyEngine.connect()
    # Read data from PostgreSQL database table and load into a DataFrame instance

    df_objet_perdu = pd.read_sql("select * from \"objet_perdu\"", dbConnection)
    dbConnection.close()


    df_objet_perdu["date"] = df_objet_perdu["date"].dt.strftime('%Y-%m-%d')

    df = df_objet_perdu.groupby(['date'])['id'].count().reset_index().rename(columns ={'date':'ds', 'id':'y'})

    train = df.drop(df.index[-5:])

    m = Prophet()
    m.fit(train)
    future = m.make_future_dataframe(periods=5, freq='D')
    forecast = m.predict(future)
    predict = forecast[['ds', 'yhat']].tail()
    return predict
    
