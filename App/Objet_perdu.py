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

city = "Lille+Europe"
URL_YEAR = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=20" \
           f"&sort=date&facet=date&refine.gc_obo_gare_origine_r_name="




class Objet_perdu(Base):
    __tablename__ = "objet_perdu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_heure_restitution = Column(DateTime())
    type = Column(String)
    gare_origine = Column(String)
    nature = Column(String)
    nom_recordtype = Column(String)
    date = Column(DateTime())

    
def import_all_objet_perdu():
    data_year = requests.get(f"{URL_YEAR}{city}")
    number_year = data_year.json().get("facet_groups")[0].get("facets")
    for each_year in number_year:
        year = each_year.get("name")
        count = each_year.get("count")
        URL = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows={count}&sort=date&facet=date&facet=gc_obo_gare_origine_r_name&refine.date={year}&refine.gc_obo_gare_origine_r_name={city}"
        data = requests.get(URL)
        for each_data in data.json().get("records"):
            session.add(
            Objet_perdu(
                date_heure_restitution=each_data.get("fields").get("gc_obo_date_heure_restitution_c"),
                type=each_data.get("fields").get("gc_obo_type_c"),
                gare_origine=each_data.get("fields").get("gc_obo_gare_origine_r_name"),
                nature=each_data.get("fields").get("gc_obo_nature_c"),
                nom_recordtype=each_data.get("fields").get("gc_obo_nom_recordtype_sc_c"),
                date=each_data.get("fields").get("date")))
    session.commit()
    lg.info('Import objet perdu done')


def init_db():
    lg.info('Drop all databases')
    Base.metadata.drop_all(engine)
    lg.info('create all databases')
    Base.metadata.create_all(engine)
