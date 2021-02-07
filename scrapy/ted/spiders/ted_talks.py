import scrapy
import re
from ted.items import TedItem
from ted.mongo_provider import MongoProvider
from datetime import datetime

class TedTalksSpider(scrapy.Spider):
    name = 'ted_talks'
    allowed_domains = ['ted.com']
    start_urls = ['https://www.ted.com/talks']

    @classmethod
    def from_crawler(cls,crawler, *args, **kwargs):
        kwargs['mongo_uri']=crawler.settings.get('MONGO_URI')
        kwargs['mongo_database']=crawler.settings.get('MONGO_DATABASE')
        return super(TedTalksSpider,cls).from_crawler(crawler,*args,**kwargs)

    def __init__(self, limit_pages=None, mongo_uri=None,mongo_database=None, *args, **kwargs):
        super(TedTalksSpider,self).__init__(*args,**kwargs)

        if limit_pages is not None:
            self.limit_pages= int(limit_pages)
        else: self.limit_pages=0

        self.mongo_provider=MongoProvider(mongo_uri,mongo_database)
        self.collection=self.mongo_provider.get_collection()
        last_items=self.collection.find().sort('uploadDate',-1).limit(1)
        self.last_scraped_url=None

    def parse(self, response):
        for video in response.css('.ga-link'):  #in ga-link there is an url of video

            url = 'https://www.ted.com'+''.join(video.css('::attr(href)').extract())     #get the url of each video
            if re.match(r".*\/talks\/.*",url) is None : continue    #checking url is proper

            if url == self.last_scraped_url:     
                print('reached last item scraped, breaking loop')
                return
            
            else: yield scrapy.Request(url, callback=self.parse_video)

        if response.css('.pagination__next'):
            next_page_url="https://www.ted.com"+"".join(response.css('.pagination__next::attr(href)').extract_first())
            match=re.match(r".*\/talks\?.*\=(\d+)",next_page_url)
            next_page_number = int(match.groups()[0])
            if next_page_number <= self.limit_pages:
                yield scrapy.Request(next_page_url)

    def parse_video(self,response):

        video = TedItem(
            con_type="ted",
            url=response.url,
            title= response.css("meta[property='og:title']::attr(content)").extract_first(),
            keywords= self.organize_keywords(response),
            author= response.css("meta[name='author']::attr(content)").extract_first(),
            description= response.css("meta[name='description']::attr(content)").extract_first(),
            uploadDate = self.change_to_datetime(response),
            views=int(response.css("meta[itemprop='interactionCount']::attr(content)").extract_first()),
            duration= self.clean_duration(response),
            languages= self.possible_languages(response),
            thumbnail= self.get_thumbnail(response)
        )

        yield(video)

    def organize_keywords(self,response):
        arr=[]
        keywords= response.css("meta[name='keywords']::attr(content)").extract_first()
        for keyword in keywords.split(","):
            arr.append(keyword.strip())
        return arr

    def change_to_datetime(self,response):
        date = response.css("meta[itemprop='uploadDate']::attr(content)").extract_first()
        return datetime.strptime(date[0:19],"%Y-%m-%dT%H:%M:%S")

    def clean_duration(self, response):
        duration=response.css("meta[itemprop='duration']::attr(content)").extract_first()
        time = duration[2:].split('M')
        minutes = int(time[0])
        seconds = int(time[1].split('S')[0])
        return str(minutes)+'m'+str(seconds)+'s'

    def possible_languages(self, response):
        arr=[]
        language=response.css("link[rel='alternate']::attr(hreflang)").extract()
        for lan in language:
            if lan == 'x-default': continue
            arr.append(lan)
        return arr

        #language=response.css(".ted-player ::attr(label)").extract()
        #for lan in language:
        #    arr.append(lan)
        #return arr

    def get_thumbnail(self, response):
        img_url=response.css("link[itemprop='thumbnailUrl']::attr(content)").extract_first()
        return response.urljoin(img_url)

