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
$ cd scrapy && scrapy crawl ted_talks -a limited_pages={as much as you want} && scrapy crawl vocal -a limited_pages={as much as you want}
</code>
</pre>

#### Web
<pre>
<code>
$ cd ../flask && python run.py
</code>
</pre>

Now hit localhost:5000 and you can see the application running.

#### Front Page
<img width="1920" alt="스크린샷 2021-02-07 03 57 58" src="https://user-images.githubusercontent.com/48878905/107135234-375e3b80-68f9-11eb-89ab-54d77515a661.png">

#### Ted Video
<img width="1920" alt="스크린샷 2021-02-07 03 58 26" src="https://user-images.githubusercontent.com/48878905/107135247-4e049280-68f9-11eb-9412-68e18564a331.png">

#### Vocal Articles
<img width="1920" alt="스크린샷 2021-02-07 03 58 48" src="https://user-images.githubusercontent.com/48878905/107135251-5ceb4500-68f9-11eb-9048-409170857f91.png">

#### Search Page
<img width="1920" alt="스크린샷 2021-02-07 03 59 08" src="https://user-images.githubusercontent.com/48878905/107135264-80ae8b00-68f9-11eb-9395-5331b9f4b59f.png">

#### Search Result
<img width="1920" alt="스크린샷 2021-02-07 03 59 28" src="https://user-images.githubusercontent.com/48878905/107135274-8dcb7a00-68f9-11eb-8854-55f916778db1.png">


## License
Distributed under the MIT License.
  
## Author
👩🏻‍🏫 Suyeon CHO

🧑🏾‍🏫 Neil-Matthieu RAMANOELINA
