# pip install requests parsel lxml
import lxml
import json
import requests
from parsel import Selector
from requests import Response


def parse(response: Response) -> list[dict]:
    selector: Selector = Selector(text=response.text)
    data: list[dict] = []

    quotes = selector.css('.quote')
    for quote in quotes:
        data.append({
            'text': quote.css('.text::text').get().strip()[1:-1],
            'author': quote.css('.author::text').get().strip(),
            'link': response.url + quote.css('span a::attr(href)').get()[1:],
            'tags': [
                {
                    'name': tag.css('::text').get().strip(),
                    'link': response.url + tag.css('::attr(href)').get()[1:]
                }
                for tag in quote.css('.tags .tag')]
        })
    return data


headers: dict[str] = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

url: str = 'https://quotes.toscrape.com'
response: Response = requests.get(url=url, headers=headers)
selector: Selector = Selector(text=response.text)

quotes_to_scrape_data = parse(response)
print(json.dumps(quotes_to_scrape_data, indent=2, ensure_ascii=False))
