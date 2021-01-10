import scrapy
import re
from datetime import datetime
from ted.mongo_provider import MongoProvider
from ted.items import TedItem, VocalItem

class VocalSpider(scrapy.Spider):
    name = 'vocal'
    allowed_domains = ['vocal.media']
    start_urls = ['https://vocal.media/']

    # def start_requests(self):
    #     for i in range(137):
    #         yield self.make_requests_from_url("https://www.ted.com/talks?page=%d" % i)

    @classmethod
    def from_crawler(cls,crawler, *args, **kwargs):
        kwargs['mongo_uri']=crawler.settings.get('MONGO_URI')
        kwargs['mongo_database']=crawler.settings.get('MONGO_DATABASE')
        return super(VocalSpider,cls).from_crawler(crawler,*args,**kwargs)

    def __init__(self, limit_pages=None, mongo_uri=None,mongo_database=None, *args, **kwargs):
        super(VocalSpider,self).__init__(*args,**kwargs)

        if limit_pages is not None:
            self.limit_pages= int(limit_pages)
        else: self.limit_pages=0

        self.mongo_provider=MongoProvider(mongo_uri,mongo_database)
        self.collection=self.mongo_provider.get_collection()
        last_items=self.collection.find().sort('uploadDate',-1).limit(1)
        self.last_scraped_url=last_items[0]['url'] if last_items.count() else None

    def parse(self, response):
        for article in response.css('.css-1ezxvls-SiteLink-PostTile'):

            url = 'https://vocal.media'+''.join(article.css('::attr(href)').extract())
            print(url)
            if re.match(r".*\/.*\/.*",url) is None : continue

            if url == self.last_scraped_url:
                print('reached last item scraped, breaking loop')
                return
            
            else: yield scrapy.Request(url, callback=self.parse_article)

        if response.css('.css-lx9tbs-SiteLink'):
            next_page_url="https://vocal.media"+"".join(response.css('.css-lx9tbs-SiteLink::attr(href)')[-3].extract())
            match=re.match(r".*\/\?page\=(\d+)",next_page_url)
            next_page_number = int(match.groups()[0])
            if next_page_number <= self.limit_pages:
                yield scrapy.Request(next_page_url)

    def parse_article(self,response):

        article = VocalItem(
            url=response.url,
            title= response.css("meta[property='og:title']::attr(content)").extract_first(),
            keywords= self.organize_keywords(response),
            author= response.css(".css-1ndema5-Text::text").extract_first(),
            description= response.css("meta[name='description']::attr(content)").extract_first(),
            uploadDate = self.change_to_datetime(response),
            image = response.css("meta[property='og:image']::attr(content)").extract_first()


        )

        yield(article)

    def organize_keywords(self,response):
        arr=[]
        keywords= response.css("meta[name='keywords']::attr(content)").extract_first()
        for keyword in keywords.split(","):
            arr.append(keyword.strip())
        return arr

    def change_to_datetime(self,response):
        date = response.css("span::attr(datetime)").extract_first()
        return datetime.strptime(date[0:19],"%Y-%m-%dT%H:%M:%S")