from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import requests
import os
import datetime


load_dotenv(override=True)

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime())
    temp = Column(Float())


def list_years():
    today = datetime.datetime.today()
    current_year = int(today.year)
    years = list(range(2014, current_year))
    return years
# print(list_years())


def dict_record(city):
    records = {}
    years = list_years()
    for year in years:
        url_year = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q" \
                   f"=&rows=10&sort=date&refine.nom={city}&refine.date={year}"
        data_year = requests.get(url_year)
        number_year = data_year.json().get("facet_groups")[1].get("facets")[0]
        year = number_year.get("name")
        count = number_year.get("count")
        records[year] = count
        records_int = {int(k): v for k, v in records.items()}
    return records_int

def list_urls(city):
    years = list_years()
    records = dict_record(city)
    urls = []

    for y in years:
        record = records[y]
        url = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&rows={record}&sort=date&facet=date&facet=nom&facet=temps_present&refine.date={y}%2F12&refine.nom={city}"
        urls.append(url)
    return urls


def import_all_weather(city):
    urls = list_urls(city)
    for url in urls:
        data = requests.get(url)
        for each_data in data.json().get("records"):
            session.add(
                Weather(
                    date=each_data.get("fields").get("date"),
                    temp=each_data.get("fields").get("tc")))
    session.commit()
    print('weather done')


def init_db():
    print('Drop all databases')
    Base.metadata.drop_all(engine)
    print('create all databases')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
    # import_all_weather(city)
