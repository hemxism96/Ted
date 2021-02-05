FROM python:3.8
COPY . .
WORKDIR /ted
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt 
ENV pages=10
ENTRYPOINT scrapy crawl ted_talks -a limited_pages=${pages} && scrapy crawl vocal -a limited_pages=${pages}