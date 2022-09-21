
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from time import sleep
import csv

start_time = time.time()

def get_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    
    
    url = f'https://www.aspshop.eu/new-items'
        
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')   
    pages_count = int(soup.find('a', class_='btn margin-0-05 no-margin-right').text)
    
     
    
    
    for page in range(1, pages_count + 1):
        url = f'https://www.aspshop.eu/new-items?page={page}&onpage=64#products'
        
        response = requests.get(url=url, headers=headers)
        
        # with open('index.html', 'w') as file:
        #     file.write(response.text)
        
        
        with open('index.html') as file:
            file.read()
        
        soup = BeautifulSoup(response.text, 'lxml')    
        
        card_url = soup.find_all('a', class_='image row center no-underline')
        
        title_item_url = []
        for item in card_url:
            item_href = 'https://www.aspshop.eu/' + item.get('href')
            title_item_url.append(item_href)
        
        # with open('item_url.json', 'w') as file:
        #     json.dump(title_item_url, file, indent=4, ensure_ascii=False)
        
        with open('item_url.json') as file:
            all_url_card = json.load(file)
        
        
        
        cards_data = []
        for item_url in all_url_card:
            
            req = requests.get(url=item_url, headers=headers)
            
            soup = BeautifulSoup(req.text, 'lxml')
            
            item_title = soup.find('li', class_='last').text.strip()
            item_img = soup.find('a', class_='col col-block padding-05 center').get('href')
            item_desc = soup.find('p', class_='description no-edges').text.strip()
            try:
                item_manufacturer = soup.find('span', class_='col col-6').find('a').text.strip()
            except:
                continue
            item_code_product = soup.find('span', class_='col col-6 break-all').text.strip()
            try:
                item_ean_product = soup.find('span', itemprop='gtin13').text.strip()
            except:
                continue
            item_weight_product_block = soup.find('span', itemprop='weight')
            item_weight_product_int = item_weight_product_block.find('span', itemprop='value').text.strip()
            try:
                item_availability = soup.find('span', class_='green').text.strip()
            except:
                item_availability = 'not available'
            
            cards_data.append(
                {
                    'title':item_title,
                    'image':item_img,
                    'description':item_desc,
                    'manufacturer':item_manufacturer,
                    'code_product':item_code_product,
                    'ean_product':item_ean_product,
                    'weight_product':item_weight_product_int,
                    'availability':item_availability
                }
            )
            sleep(2)
            print(f'Обработано {page}/{pages_count}')
            
            # with open(f'aspshop_{cur_time}.json', 'w') as file:
            #     json.dump(cards_data, file, indent=4, ensure_ascii=False)

                
    
    

def main():
    get_data()
    finish_time = time.time() - start_time
    print(f'Затраченное на обработку времени: {finish_time}')

if __name__ == '__main__':
    main()
    