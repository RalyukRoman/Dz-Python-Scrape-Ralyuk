# pip install requests parsel json
import json
import requests
from parsel import Selector, SelectorList
from requests import Response

class BooksToScrapeParse():
    def __init__(self, url: str) -> None:
        self.url = url
        self.next_button_url = url
        self.headers = self.get_headers()
        self.response = self.make_request()

    def get_headers(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def make_request(self, url: str | None = None) -> Response:
        if url is None:
            url = self.url
        return requests.get(url=url, headers=self.headers)

    def parse(self, data: list[dict] | None = None, url: str | None = None) -> list[dict]:
        if data is None:
            data = []
        if url is None:
            url = self.url
        self.response = self.make_request(url=url)
        selector: Selector = Selector(text=self.response.text)
        ol: SelectorList = selector.css('ol > li')
        for li in ol:
            title: str = li.css('h3 a::attr(title)').get().strip()
            image: str = url + li.css('.image_container a img::attr(src)').get()
            link: str = url + li.css('.image_container a::attr(href)').get()[1:]
            rating: int = sum([['Zero', 'One', 'Two', 'Three', 'Four', 'Five'].index(i)
                    if i in ['Zero', 'One', 'Two', 'Three', 'Four', 'Five'] else 0
                    for i in li.css('p::attr(class)').get().strip().split(' ')])
            price: str = li.css('.price_color::text').get().strip().replace("Â", "")
            stock: str = 'In stock' if li.css('p.instock.availability i::attr(class)').get().strip() == "icon-ok" else 'Not stock'
            position: int = ol.index(li) + 1
            data.append({
                        'title': title,
                        'image': image,
                        'link': link,
                        'rating': rating,
                        'price': price,
                        'stock': stock,
                        'position': position
                })
        if selector.css('.pager .next a::attr(href)').get():
            self.next_button_url = (self.url + 'catalogue/' + selector.css('.pager .next a::attr(href)').get().replace("catalogue/", ""))
        else:
            self.next_button_url = None
        return data

    def all_parse(self) -> list[dict]:
        self.next_button_url = self.url
        data = []
        while True:
            if self.next_button_url:
                data = self.parse(data=data, url=self.next_button_url)
            else:
                self.next_button_url = self.url
                return data
                break
    def print(self, data: list[dict]) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))


btsp = BooksToScrapeParse(url='https://books.toscrape.com/')
books_to_scrape_parse: list[dict] = btsp.all_parse()
btsp.print(books_to_scrape_parse)