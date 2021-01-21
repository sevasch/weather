# Weather scraper
This script gathers meteorological data from various sources and saves it locally. The idea is to collect data over a long period of time. It was designed to run permanently on a Raspberry Pi.  

## Data
| data                       | interval | source                                                              |
|----------------------------|----------|---------------------------------------------------------------------|
| weather map                | 6h       | http://www.hossi-im-netz.de/wordpress/vorhersage/bodendruckkarte/   |
| IR satellite images        | 1h       | https://www.wetterdienst.de/Europawetter/Satellitenbilder/Infrarot/ |
| significant weather charts | 6h       | http://www.lennuilm.ee/prognoosiinfo/kaardid/wafc-euroopa-kaardid/  |
| METAR                      | 1h       | https://www.meteoschweiz.admin.ch/                                  |
| TAF                        | 1h       | https://www.meteoschweiz.admin.ch/                                  |
| emagram Payerne            | 12h      | https://www.meteoschweiz.admin.ch/                                  |
| wind charts                | 1d       | https://maercu.ch/aviation/                                         |


## Options
<table>
    <tr>
        <td>--target_dir</td>
        <td>All data will be saved to this directory. </td>
    </tr>
</table>


## Hardware requirements and dependencies
* Raspberry Pi (runs fine on Model 2B) with permanent power and internet connection. 
* Storage medium with at least 10GB free space
* Python 3.7 or higher with packes described in __requirements.txt__

## Setup
I recommend using a cronjob to execute __scrapy.py__ every hour +30 minutes. 

Open the crontab file: 
```
crontab -e
```
Append the following line to the document: 
```
30 * * * * python3 your_directory/scrape.py --target_dir where_to_save_data
```
Then, save and exit the file and check if everything is working correctly. The files should appear in individual folders and be named with date and time. I recommend backing up the data from time to time. 