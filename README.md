# Ted Talks and Vocal
This project is for making a website using data scraped from the original site.

We used scrapy for crawling, flask for the web, elasticsearch for search engine, mongo for db, and docker for containerization.

## Prerequisites
- Python 3.8
- Docker
- mongodb

## Install
<pre>
<code>
$ pip3 install -r requirements.txt
</code>
</pre>

## Usage
<pre>
<code>
$ git clone https://github.com/hemxism96/Ted-Talks-Vocal.git
</code>
</pre>

#### Docker
<pre>
<code>
$ docker-compose up -d
</code>
</pre>
  
#### Scrapy
We recommend at least 100 pages per site.
<pre>
<code>
$ cd scrapy cd scrapy && scrapy crawl ted_talks -a limited_pages={as much as you want} && scrapy crawl vocal -a limited_pages={as much as you want}
</code>
</pre>

#### Web
<pre>
<code>
$ cd ../flask && python run.py
</code>
</pre>

Now hit localhost:5000 and you can see the application running.

## License
Distributed under the MIT License.
  
## Author
👩🏻‍🏫 Suyeon CHO

🧑🏾‍🏫 Neil-Matthieu RAMANOELINA
