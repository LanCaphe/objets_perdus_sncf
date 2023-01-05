from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import requests
import os
import logging as lg
load_dotenv(override=True)


SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

city = "LILLE"
URL_GARE_DEPART = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-tgv-aqst&q=&sort=date&facet=date&facet=service&facet=gare_depart&facet=gare_arrivee&refine.gare_depart="
URL_GARE_ARRIVEE = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-tgv-aqst&q=&sort=date&facet=date&facet=service&facet=gare_depart&facet=gare_arrivee&refine.gare_arrivee="

class Regularite(Base):
    __tablename__ = "regularite"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nb_train_prevu = Column(Integer)
    gare_arrivee = Column(String)
    gare_depart = Column(String)
    date = Column(String)
    
def import_all_Regularite_gare_depart():
    data_year = requests.get(f"{URL_GARE_DEPART}{city}")
    number_year = data_year.json().get("facet_groups")[0].get("facets")
    for each_year in number_year:
        year = each_year.get("name")
        URL = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-tgv-aqst&q=&sort=date&facet=date&facet=service&facet=gare_depart&facet=gare_arrivee&refine.date={year}&refine.gare_depart={city}"
        data = requests.get(URL)
        for each_data in data.json().get("records"):
            session.add(
            Regularite(
                nb_train_prevu=each_data.get("fields").get("nb_train_prevu"),
                gare_arrivee=each_data.get("fields").get("gare_depart"),
                gare_depart=each_data.get("fields").get("gare_arrivee"),
                date=each_data.get("fields").get("date")))
    session.commit()
    lg.info('Import gare depart de lille done')
    
    
def import_all_Regularite_gare_arrivee():
    data_year = requests.get(f"{URL_GARE_ARRIVEE}{city}")
    number_year = data_year.json().get("facet_groups")[0].get("facets")
    for each_year in number_year:
        year = each_year.get("name")
        URL = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-tgv-aqst&q=&sort=date&facet=date&facet=service&facet=gare_depart&facet=gare_arrivee&refine.date={year}&refine.gare_arrivee={city}"
        data = requests.get(URL)
        for each_data in data.json().get("records"):
            session.add(
            Regularite(
                nb_train_prevu=each_data.get("fields").get("nb_train_prevu"),
                gare_arrivee=each_data.get("fields").get("gare_depart"),
                gare_depart=each_data.get("fields").get("gare_arrivee"),
                date=each_data.get("fields").get("date")))
    session.commit()
    lg.info('Import gare arrivee à Lille done')
                
def init_db():
    lg.info('Drop all databases')
    Base.metadata.drop_all(engine)
    lg.info('create all databases')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
    import_all_Regularite_gare_depart()
    import_all_Regularite_gare_arrivee()