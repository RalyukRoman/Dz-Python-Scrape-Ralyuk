# pip install requests parsel lxml json
import lxml
import json
import requests
from parsel import Selector
from requests import Response


def parse(response: Response) -> list[dict]:
    selector: Selector = Selector(text=response.text)
    data: list[dict] = []

    ol = selector.css('ol > li')
    for li in ol:
        data.append({
            'title': li.css('h3 a::attr(title)').get().strip(),
            'image': response.url + li.css('.image_container a img::attr(src)').get(),
            'link': response.url + li.css('.image_container a::attr(href)').get()[1:],
            'rating': sum([['Zero', 'One', 'Two', 'Three', 'Four', 'Five'].index(i)
                       if i in ['Zero', 'One', 'Two', 'Three', 'Four', 'Five'] else 0
                       for i in li.css('p::attr(class)').get().strip().split(' ')]),
            'price': li.css('.price_color::text').get().strip().replace("Â", ""),
            'stock': 'In stock' if li.css('p.instock.availability i::attr(class)').get().strip() == "icon-ok" else 'Not stock',
            'position': ol.index(li) + 1
        })
    return data


headers: dict[str] = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

url: str = 'https://books.toscrape.com/'
response: Response = requests.get(url=url, headers=headers)
selector: Selector = Selector(text=response.text)

quotes_to_scrape_data = parse(response)
print(json.dumps(quotes_to_scrape_data, indent=2, ensure_ascii=False))
