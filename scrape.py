import time
import numpy as np
import datetime
import logging
from os import path
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='meteoscraping.log', level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

folder = '/home/pi/share/meteo/'
# folder = ''

attempttime = str(datetime.datetime.now())  # get current time

# BODENDRUCKKARTE (alle 6h)
url = "http://www.hossi-im-netz.de/wordpress/vorhersage/bodendruckkarte/"
r = requests.get(url) # open webpage
soup = BeautifulSoup(r.content, features="html.parser") # get

hours = str(np.floor(int(attempttime[11:13])/6).astype(int)*6) # round hours down to last 6
if len(hours) < 2:
    hours = "0" + hours
timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + hours + "00"

try:
    image_url = soup.find_all('img', {'class': 'alignnone size-full'})[0].get_attribute_list('src')[0]
    dt = str(image_url)[str(image_url).rfind(".", -5):]

    if not path.exists(folder + "Bodendruckkarte/" + timestamp + "_Bodendruckkarte" + dt):
        img_data = requests.get(image_url).content
        with open(folder + "Bodendruckkarte/" + timestamp + "_Bodendruckkarte" + dt, 'wb') as handler:
            handler.write(img_data)

        logging.info(attempttime + " Bodendruckkarte saved")
    else:
        logging.info(attempttime + " Bodendruckkarte already exists")

except:
    logging.warning(attempttime + " scraping of Bodendruckkarte failed")


# SWC (alle 6h)
current_hour = str(np.floor(int(attempttime[11:13])/6).astype(int)*6) # round hours down to last 6
if len(hours) < 2:
    current_hour = "0" + current_hour
current_day = int(attempttime[8:10])

if hours == "00":
    url = "http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-12-utc/?lang=en"
    day = current_day
    hour = "12"
elif hours == "06":
    url = "http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-18-utc/?lang=en"
    day = current_day
    hour = "18"
elif hours == "12":
    url = "http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-00-utc/?lang=en"
    day = current_day + 1
    hour = "00"
elif hours == "18":
    url = "http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-06-utc/?lang=en"
    day = current_day + 1
    hour = "06"

day = str(day)
if len(day) < 2:
    day = "0" + day
timestamp = attempttime[0:4] + attempttime[5:7] + day + "_" + hour + "00"

r = requests.get(url) # open webpage
soup = BeautifulSoup(r.content, features="html.parser") # get


try:
    image_url = soup.find_all('img')[0].get_attribute_list('src')[0]
    dt = str(image_url)[str(image_url).rfind(".", -5):]

    if not path.exists(folder + "SWC/" + timestamp + "_SWC" + dt):
        img_data = requests.get(image_url).content
        with open(folder + "SWC/" + timestamp + "_SWC" + dt, 'wb') as handler:
            handler.write(img_data)

        logging.info(attempttime + " SWC saved")
    else:
        logging.info(attempttime + " SWC already exists")

except:
    logging.warning(attempttime + " scraping of SWC failed")




# WINDKARTEN (taeglich)

class MeteoSource:
    def __init__(self, name, url, freq):
        self.name = name
        self.url = url
        self.freq = freq

sources = []
sources.append(MeteoSource("Wind_FL050", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL050&nr=0", "1d"))
sources.append(MeteoSource("Wind_FL100", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL100&nr=0", "1d"))
sources.append(MeteoSource("Wind_FL140", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL140&nr=0", "1d"))
sources.append(MeteoSource("Wind_FL180", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL180&nr=0", "1d"))
sources.append(MeteoSource("Wind_FL240", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL240&nr=0", "1d"))
sources.append(MeteoSource("Wind_FL300", "https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL300&nr=0", "1d"))

for source in sources:
    r = requests.get(source.url) # open webpage
    soup = BeautifulSoup(r.content, features="html.parser") # get contents

    if source.freq == "6h":
        hours = str(np.floor(int(attempttime[11:13])/6).astype(int)*6) # round hours down to last 6
        if len(hours) < 2:
            hours = "0" + hours
        timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + hours + "00"

    elif source.freq == "1h":
        hours = str(attempttime[11:13])
        if len(hours) < 2:
            hours = "0" + hours
        timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + hours + "00"

    elif source.freq == "15min":
        mins = str(np.floor(int(attempttime[14:16])/15).astype(int)*15) # round mins down to last 15
        if mins == "0":
            mins = "00"
        timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + attempttime[11:13] + mins

    elif source.freq == "1d":
        timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10]

    try:
        image_url = soup.find("div").find("img").get_attribute_list('src')[0]
        dt = str(image_url)[str(image_url).rfind(".", -5):]

        if not path.exists(folder + source.name + "/" + timestamp + "_" + source.name + dt):
            img_data = requests.get(image_url).content
            with open(folder + source.name + "/" + timestamp + "_" + source.name + dt, 'wb') as handler:
                handler.write(img_data)

            logging.info(attempttime + " " + source.name + " saved")
        else:
            logging.info(attempttime + " " + source.name + " already exists")

    except:
        logging.warning(attempttime + " scraping of " + source.name + " failed")


# METAR / TAF
hours = str(attempttime[11:13])
if len(hours) < 2:
    hours = "0" + hours
timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + hours + "00"

url = "https://www.meteoschweiz.admin.ch/home/service-und-publikationen/beratung-und-service/flugwetter/metar-taf.html"

r = requests.get(url) # open webpage
soup = BeautifulSoup(r.content, features="html.parser") # get contents

try:
    tables = soup.find_all('pre', {'class': 'monospace'})

    # get METAR
    if not path.exists(folder + "METAR/" + timestamp + "_METAR.txt"):
        metar_file = open(folder + "METAR/" + timestamp + "_METAR.txt", "w")
        n = metar_file.write(tables[0].decode_contents())
        metar_file.close()

        logging.info(attempttime + " METAR saved")
    else:
        logging.info(attempttime + " METAR already exists")

    # get TAF
    if not path.exists(folder + "TAF/" + timestamp + "_TAF.txt"):
        taf_file = open(folder + "TAF/" + timestamp + "_TAF.txt", "w")
        n = taf_file.write(tables[1].decode_contents())
        taf_file.close()

        logging.info(attempttime + " TAF saved")
    else:
        logging.info(attempttime + " TAF already exists")

except:
    logging.warning(attempttime + " scraping of METAR and TAF failed")


# EMAGRAMM (alle 12h) 6930
current_day = int(attempttime[8:10])
if int(attempttime[11:13]) < 12:
    hour = '12'
    day = current_day - 1
else:
    hour = '00'
    day = current_day

day = str(day)
if len(day) < 2:
    day = "0" + day
timestamp = attempttime[0:4] + attempttime[5:7] + day + "_" + hour + "00"

url = "https://www.meteoschweiz.admin.ch/product/input/radio-soundings/VSST76.LSSW_" + timestamp + ".txt"

r = requests.get(url) # open webpage
soup = BeautifulSoup(r.content, features="html.parser") # get contents

try:
    if not path.exists(folder + "Emagramme/" + timestamp + "_Emagramm.txt"):
        file = open(folder + "Emagramme/" + timestamp + "_Emagramm.txt", "w")
        n = file.write(soup.decode_contents())
        file.close()

        logging.info(attempttime + " Emagramm saved")
    else:
        logging.info(attempttime + " Emagramm already exists")

except:
    logging.warning(attempttime + " scraping of " + "Emagramm_Payerne" + " failed")




# SAT IR & VIS (alle 1h)
url = "https://www.wetterdienst.de/Europawetter/Satellitenbilder/Infrarot/"
r = requests.get(url) # open webpage
soup = BeautifulSoup(r.content, features="html.parser") # get

hours = str(attempttime[11:13])
if len(hours) < 2:
    hours = "0" + hours
timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + "_" + hours + "00"

try:
    image_url = "http://" + soup.find_all('a', {'class': 'cboxElement'})[0].get_attribute_list('href')[0][2:]
    dt = str(image_url)[str(image_url).rfind(".", -5):]

    if not path.exists(folder + "SAT/" + timestamp + "_SAT" + dt):
        img_data = requests.get(image_url).content
        with open(folder + "SAT/" + timestamp + "_SAT" + dt, 'wb') as handler:
            handler.write(img_data)

        logging.info(attempttime + " SAT saved")
    else:
        logging.info(attempttime + " SAT already exists")

except:
    logging.warning(attempttime + " scraping of SAT failed")
