from App import Objet_perdu, Regularite, Weather

import pycron
import time
import logging as lg

def cron():
    while True:
        if pycron.is_now('0 0 * * 0'):
                app()
        time.sleep(60)

def app():
    timenow = time.localtime()
    lg.info('delete et create database for objet perdu', str( time.strftime("%H:%M", timenow)))
    Objet_perdu.init_db()
    lg.info('Import Objet perdu')
    Objet_perdu.import_all_objet_perdu()
    Weather.import_all_weather("LILLE-LESQUIN")

    Weather.import_all_weather("LILLE-LESQUIN")

    Regularite.import_all_Regularite_gare_depart()
    Regularite.import_all_Regularite_gare_arrivee()

if __name__ == '__main__':
    lg.info('the programs is launch')
    print('the programs is launch')
    cron()

    
    
