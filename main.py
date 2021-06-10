
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import requests
from bs4 import BeautifulSoup
import json
import time
import csv


class ZillowScraper():
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'zguid=23|%24601b12dd-51d9-492a-83d8-e3a69fed3f20; zjs_user_id=null; _ga=GA1.2.2133127305.1613171125; zjs_anonymous_id=%22601b12dd-51d9-492a-83d8-e3a69fed3f20%22; _pxvid=ca8fe1df-6d86-11eb-9758-0242ac120018; _gcl_au=1.1.1692965813.1613171126; _fbp=fb.1.1613171126268.2056717825; _pin_unauth=dWlkPVlqUXlNMlV5TlRJdFpURXlNeTAwTVRjekxUaGpNakl0TVdaallUSTFPR0U0T1dWaw; ki_r=; __gads=ID=e2704d216e522cb1:T=1613171142:S=ALNI_MYZVQab4mStnd9JVxscB_Eb5r8LXg; ki_s=; _gac_UA-21174015-56=1.1613729823.Cj0KCQiA4L2BBhCvARIsAO0SBdZ6I29xJVtgZfTJpBKwDO7Mi5NNzjrnmk9VM95OPL8sfEwBMvdkWSkaArR7EALw_wcB; _gcl_aw=GCL.1613729825.Cj0KCQiA4L2BBhCvARIsAO0SBdZ6I29xJVtgZfTJpBKwDO7Mi5NNzjrnmk9VM95OPL8sfEwBMvdkWSkaArR7EALw_wcB; G_ENABLED_IDPS=google; g_state={"i_p":1613868568434,"i_l":2}; zgsession=1|f30b1470-1b71-432a-9d35-d51ed32c228d; KruxPixel=true; DoubleClickSession=true; KruxAddition=true; ki_t=1613171142543%3B1614974724857%3B1614974759623%3B2%3B15; _gid=GA1.2.252832672.1615177139; JSESSIONID=88A043335B2BC337F60184E17EBD15D2; _derived_epik=dj0yJnU9X1kxanVxVldZRFQxcW92OG9xZVUzdERocGpPdHFQT0Qmbj1Ua2ZkVnFBVE00SEs0Qk8wcWo5TklRJm09MSZ0PUFBQUFBR0JGcjYwJnJtPTEmcnQ9QUFBQUFHQkZyNjA; search=6|1617771886205%7Cregion%3Dboston-ma%26rect%3D43.36%252C-70.07%252C41.36%252C-72.07%26disp%3Dmap%26mdm%3Dauto%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26rs%3D0%26ah%3D0%09%0944269%09%09%09%09%09%09; AWSALB=E4JPzVHtZk5FwUSgXgi/YWmXffI3dXph/inQBgbBljpg7rfePEV7LfMCfxoJV0mjEcIYSGbQ9+V0AylWlooOX4ltA4PWUt6d/5xQ7gQ7a0E8NLNuX/4I9eoNSzpL; AWSALBCORS=E4JPzVHtZk5FwUSgXgi/YWmXffI3dXph/inQBgbBljpg7rfePEV7LfMCfxoJV0mjEcIYSGbQ9+V0AylWlooOX4ltA4PWUt6d/5xQ7gQ7a0E8NLNuX/4I9eoNSzpL; _uetsid=67f773607fc511eb9fbc6d1263168d71; _uetvid=cae5e8606d8611ebac26e9557d420e90; _px3=19b76fcbfd1e89f73783f63dc505760feaab4eec2c5d19ef9615b8d228094656:f6kwpWlM/HtoB0C2VNhP0VlzVJEi1i2WA9Ml9lvFl0YpRLY3gIxbh8OluIOO4Cdj53AHk9WuKYH8jhvqFyDQyQ==:1000:IomS0U7jT4MuDVyURFDnHRLQOTAkS8OHYW56QPhNMnhX8rWPj0qVGSt1ebNj3XNsRp6J87SCgwoc8tNlVS1+79wDWKOsG6d+vWjW/mtVoDZNIRnT2YCRZtwySCZrFayoW9xBdnRoNxj7OjQA1ZGGbsSFJDZuryPPRNavcsTQEL8=',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print("inside fetch")
        print(response.status_code)
        return response

    def parse(self, response):
        content = BeautifulSoup(response,'lxml')
        #print(content.prettify())
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        #print(deck.prettify())
        if deck is not None:
            for card in deck.contents:
                script = card.find('script', {'type': 'application/ld+json'})
                if script:
                    script_json = json.loads(script.contents[0])
                    #print(script_json)
                    if script_json['geo']['latitude'] is None:
                        script_json['geo']['latitude'] = 0
                    if script_json['geo']['longitude'] is None:
                        script_json['geo']['longitude'] = 0
                    if script_json['floorSize']['value'] is None:
                        script_json['floorSize']['value'] = 0
                    if script_json['url'] is None:
                        script_json['url'] = 0
                    if script_json['address'] is None:
                        script_json['address'] = 0
                    if script_json['name'] is None:
                        script_json['name'] = 0
                    self.results.append({
                        'latitude': script_json['geo']['latitude'],
                        'longitude': script_json['geo']['longitude'],
                        'floorSize': script_json['floorSize']['value'],
                        'url': script_json['url'],
                        'address': script_json['address'],
                        'name': script_json['name'],
                        'price': card.find('div', {'class': 'list-card-price'}).text
                    })


    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            print(self.results[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = 'https://www.zillow.com/homes/Boston/'
        i=1
        for page in list(range(20)):
            print(i)
            i=i+1
            params ={
                'searchQueryState': '{"pagination":{"currentPage": %s},"mapBounds":{"west":-71.20727008056642,"east":-70.8879799194336,"south":42.21535836951816,"north":42.4113521776861},"regionSelection":[{"regionId":44269,"regionType":6}],"isMapVisible":false,"filterState":{"ah":{"value":true},"pnd":{"value":true},"abo":{"value":true}},"isListVisible":true,"mapZoom":12}' %page
            }
            res = self.fetch(url, params)
            if i != 10:
                self.parse(res.text)
            time.sleep(3)
        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()
