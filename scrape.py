import os
import argparse
import numpy as np
import datetime
import logging
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='weather scraping module')
parser.add_argument('--target_dir', default='test', help='where to save files')
args = parser.parse_args()

os.makedirs(args.target_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(args.target_dir, 'meteoscraping.log'),
                    level=logging.INFO, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


''' FUNCTIONS '''
def write_file(data, subdir, filename):
    dir = os.path.join(args.target_dir, subdir)
    os.makedirs(dir, exist_ok=True)
    file = os.path.join(dir, filename)
    print(file)
    if not os.path.exists(file):
        dt = file.split('.')[-1]
        with open(file, 'wb' if dt in ['jpg', 'png'] else 'w') as handler:
            handler.write(data)
        logging.info('{} saved in {}'.format(filename, dir))
    else:
        logging.info('{} already exists'.format(filename))

''' MAIN '''
if __name__ == '__main__':
    attempttime = str(datetime.datetime.now())  # get current time

    # WEATHER CHARTS (every 6h)
    url = 'http://www.hossi-im-netz.de/wordpress/vorhersage/bodendruckkarte/'
    soup = BeautifulSoup(requests.get(url).content, features='html.parser')  # get

    hours = str(np.floor(int(attempttime[11:13])/6).astype(int)*6)  # round hours down to last 6
    if len(hours) < 2:
        hours = '0' + hours
    timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + '_' + hours + '00'

    try:
        image_url = soup.find_all('img', {'class': 'alignnone size-full'})[0].get_attribute_list('src')[0]
        dt = str(image_url)[str(image_url).rfind('.', -5):]
        img_data = requests.get(image_url).content
        write_file(img_data, 'Bodendruckkarte', timestamp + '_Bodendruckkarte' + dt)
    except:
        logging.warning('scraping of Bodendruckkarte failed')


    # SWC (every 6h)
    current_hour = str(np.floor(int(attempttime[11:13])/6).astype(int)*6) # round hours down to last 6
    if len(hours) < 2:
        current_hour = '0' + current_hour
    current_day = int(attempttime[8:10])

    if hours == '00':
        url = 'http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-12-utc/?lang=en'
        day = current_day
        hour = '12'
    elif hours == '06':
        url = 'http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-18-utc/?lang=en'
        day = current_day
        hour = '18'
    elif hours == '12':
        url = 'http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-00-utc/?lang=en'
        day = current_day + 1
        hour = '00'
    elif hours == '18':
        url = 'http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/sigwx-euroopa-06-utc/?lang=en'
        day = current_day + 1
        hour = '06'

    day = str(day)
    if len(day) < 2:
        day = '0' + day
    timestamp = attempttime[0:4] + attempttime[5:7] + day + '_' + hour + '00'

    r = requests.get(url) # open webpage
    soup = BeautifulSoup(r.content, features='html.parser') # get

    try:
        image_url = soup.find_all('img')[0].get_attribute_list('src')[0]
        dt = str(image_url)[str(image_url).rfind('.', -5):]
        img_data = requests.get(image_url).content
        write_file(img_data, 'SWC', timestamp + '_SWC' + dt)
    except:
        logging.warning('scraping of SWC failed')

    # WIND CHARTS (daily)
    names = ['Wind_FL050', 'Wind_FL100', 'Wind_FL140', 'Wind_FL180', 'Wind_FL240', 'Wind_FL300']
    urls = ['https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL050&nr=0',
            'https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL100&nr=0',
            'https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL140&nr=0',
            'https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL180&nr=0',
            'https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL240&nr=0',
            'https://maercu.ch/aviation/imageDisplay/imageDisplay.php?content=windTmpFL300&nr=0']

    for name, url in zip(names, urls):
        r = requests.get(url)  # open webpage
        soup = BeautifulSoup(r.content, features='html.parser') # get contents
        timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10]

        try:
            image_url = soup.find('div').find('img').get_attribute_list('src')[0]
            dt = str(image_url)[str(image_url).rfind('.', -5):]
            img_data = requests.get(image_url).content
            write_file(img_data, name, timestamp + '_' + name + dt)
        except:
            logging.warning('scraping of ' + name + ' failed')


    # METAR / TAF (every 1h)
    hours = str(attempttime[11:13])
    if len(hours) < 2:
        hours = '0' + hours
    timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + '_' + hours + '00'

    url = 'https://www.meteoschweiz.admin.ch/home/service-und-publikationen/beratung-und-service/flugwetter/metar-taf.html'

    r = requests.get(url) # open webpage
    soup = BeautifulSoup(r.content, features='html.parser') # get contents

    try:
        tables = soup.find_all('pre', {'class': 'monospace'})
        write_file(tables[0].decode_contents(), 'METAR', timestamp + '_METAR.txt')
        write_file(tables[1].decode_contents(), 'TAF', timestamp + '_TAF.txt')
    except:
        logging.warning('scraping of METAR and TAF failed')


    # EMAGRAMM (every 12h)
    current_day = int(attempttime[8:10])
    if int(attempttime[11:13]) < 12:
        hour = '12'
        day = current_day - 1
    else:
        hour = '00'
        day = current_day

    day = str(day)
    if len(day) < 2:
        day = '0' + day
    timestamp = attempttime[0:4] + attempttime[5:7] + day + '_' + hour + '00'

    url = 'https://www.meteoschweiz.admin.ch/product/input/radio-soundings/VSST76.LSSW_' + timestamp + '.txt'

    r = requests.get(url) # open webpage
    soup = BeautifulSoup(r.content, features='html.parser') # get contents

    try:
        path = os.path.join(args.target_dir, 'Emagramme', timestamp + '_Emagramm.txt')
        write_file(soup.decode_contents(), 'Emagramme', timestamp + '_Emagramm.txt')
    except:
        logging.warning('scraping of Emagramm failed')


    # SAT IR (every 1h)
    url = 'https://www.wetterdienst.de/Europawetter/Satellitenbilder/Infrarot/'
    r = requests.get(url) # open webpage
    soup = BeautifulSoup(r.content, features='html.parser') # get

    hours = str(attempttime[11:13])
    if len(hours) < 2:
        hours = '0' + hours
    timestamp = attempttime[0:4] + attempttime[5:7] + attempttime[8:10] + '_' + hours + '00'

    try:
        image_url = 'http://' + soup.find_all('a', {'class': 'cboxElement'})[0].get_attribute_list('href')[0][2:]
        dt = str(image_url)[str(image_url).rfind('.', -5):]
        write_file(requests.get(image_url).content, 'SAT', timestamp + '_SAT' + dt)
    except:
        logging.warning('scraping of SAT failed')
