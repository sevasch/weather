CONTAINERNAME=weather_scraper
IMAGENAME=weather_scraper
VERSION=latest

DATA_PATH=$(shell pwd)/data

init:
	mkdir -p ${DATA_PATH}

build:
	docker build -t ${IMAGENAME}:${VERSION} .

run:
	docker run -d -v ${DATA_PATH}:/data --name ${CONTAINERNAME}  ${IMAGENAME}:${VERSION}

start:
	docker start ${CONTAINERNAME}

stop:
	docker stop ${CONTAINERNAME}

remove:
	docker rmi -f ${CONTAINERNAME}
	docker rm -f ${CONTAINERNAME}

shell: 
	docker exec -it ${CONTAINERNAME} bash