import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['stroypark.su']
    start_urls = ['http://stroypark.su/']
    pages_count = 100  # сколько всего страниц в категории

    def start_requests(self):
        def lines(nm):
            with open(nm, 'r', encoding='utf8') as f:
                for line in f:
                    yield line

        for link in lines('/media/mugichu/Transcend/ParserScrapy/stroypark/stroypark/list.txt'):
            # вбивайте ссылки в файл построчно
            for page in range(0, 1 + self.pages_count):
                urls = link
                url = f'{urls}?page={page}'
                yield scrapy.Request(url, callback=self.parse_pages)
            # ставиться после url meta={'proxy': '217.6.21.170:8080'},
            # так как ip сервера Германии то происходят timeouts если и брать прокси то из РФ
            # в meta вписан прокси через который идет запрос

    def parse_pages(self, response, **kwargs):
        for href in response.css('.c-good-item-content .c-good-item-more::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'Название': response.css('.c-good-title::text').extract_first('').strip(),
            'Артикул': response.css('.c-good-code strong::text').extract_first('').strip(),
            'Категория': response.css('.c-breadcrumb .c-layout a::text').extract(),
            'Цена без карты': response.css('.c-good-prices strong::text').extract_first('').strip(),
            'Цена с картой': response.css('.c-good-prices .o-highlight::text').extract_first('').strip(),
        }
        yield item

# команда для запуска парсера
# scrapy crawl catalog -O (название).(формат)
# пример scrapy crawl catalog -O dump.csv
