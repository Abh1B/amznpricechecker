import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

toaster = ToastNotifier()

def get_search_url():
    search = input("Enter Product: ")
    search_lists = search.split()
    amzn = "https://amazon.com.au"
    return amzn + '/s?k=' + '+'.join(search_lists) + '&ref=nb_sb_noss'

def tracker(url, search, random_header):
    try:
        url_open = requests.get(url, headers=random_header)
        soup = BeautifulSoup(url_open.content, 'html.parser')
        tag = soup('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        tag_2 = soup('span', {'class': 'a-price-whole'})
        
        for name, price in zip(tag, tag_2):
            if search.lower() in name.text.lower():
                print("{} | price: {} AU$".format(name.text, price.text))
                if name.text in product_prices:
                    if price.text < product_prices[name.text]:
                        toaster.show_toast("Price Drop", "{} | Price: {}".format(name.text, price.text))
                product_prices[name.text] = price.text
    except requests.RequestException as e:
        print("Error fetching data:", e)

product_prices = {}

while True:
    search_url = get_search_url()
    user = UserAgent()
    random_header = {'User-Agent': str(user.random)}
    print('Checking.....', time.asctime(time.localtime(time.time())))
    tracker(search_url, search_url.split('=')[-1].split('&')[0].replace('+', ' '), random_header)
    time.sleep(60 * 3)  # 3 minutes
