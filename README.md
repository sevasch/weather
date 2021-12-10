# Weather scraper
The idea of this project is to collect meteorological data from various sources over long time periods. It is designed to run on devices with low power consumption such as _Raspberry Pi_ but can also be run on any other system as docker container. 

The intent behind collecting a lot of meteorological data was originally to create animations for meteorology lessons during flight training. This project also served as an exercise on Linux, Docker and Pyton. 

Future changes might include: 
* Improvements in logging. 
* Network storage to access data. 
* Testing and better exception handling. 
* Making the Python code more readable and splitting it up. 

## Data overview
The data is collected from various sources. 
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


## Hardware requirements
All code was tested on a _Raspberry Pi 2B_. To ensure completeness of the scraped data, I highly recommend permanent power supply and internet connection. It is also a good idea to use a large (10GB+) so the system can run for longer before storage runs out. 

## Setup using Docker
First of all, make sure that docker and make are installed: 
```
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install docker
```

The docker installation can be checked as follows: 

```
sudo docker run hello-world
sudo docker images
```

Running the second command should display a list containing the __hello-world__ repository. 

Next, we will use __make__ to initialize, build, run and start the docker container. Run the following commands from the repository directory on the machine you wish to use as permanent weather scraper. 


```
make init
make build
make run
make start
```

After some time, you should be able to find the scraped files in the __data__ directory named with date and time. 

To stop the container, type the following: 

```
make stop
```

While debugging, one might wish to remove all containers (while they are stopped). 

```
make remove
```

To access the shell of the container, type

```
make shell
```

## Alternative setup (running directly on machine)
Make sure, Python 3.6 or higher and the dependencies mentioned in __requirements.txt__ are installed. 

Set up a cronjob to execute __scrapy.py__ every hour +30 minutes. To do so, open the crontab file: 
```
crontab -e
```
Append the following line to the document: 
```
30 * * * * python3 your_directory/scrape.py --target_dir where_to_save_data
```
Then, save and exit the file and check if everything is working correctly. The files should appear in individual folders and be named with date and time. I recommend backing up the data from time to time. 
