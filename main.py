from App import Objet_perdu, Weather
import pycron
import time

def cron():
    while True:
        if pycron.is_now('0 0 * * 0'):
                app()
        time.sleep(60)

def app():
    timenow = time.localtime()
    print('delete et create database for objet perdu', str( time.strftime("%H:%M", timenow)))
    Objet_perdu.init_db()
    print('Import Objet perdu')
    Objet_perdu.import_all_objet_perdu()
    Weather.import_all_weather("LILLE-LESQUIN")

if __name__ == '__main__':
    cron()

    
    
