import requests
from bs4 import BeautifulSoup
import csv
from threading import Timer


def write_to_csv(data):
    with open('data_from_kivano.csv', 'a') as file:
        write = csv.writer(file)
        write.writerow([data['title'], data['price'], data['img']])


def get_html(url):
    response = requests.get(url)
    # print(response.text)
    return response.text

# get_html('https://www.kivano.kg/mobilnye-telefony')


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div', class_='pager-wrap').find('ul', class_='pagination-sm').find_all('li')
    last_page = page_list[-1].text
    # print(last_page)
    return int(last_page)

get_total_pages(get_html('https://www.kivano.kg/mobilnye-telefony'))

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find('div', class_='list-view').find_all('div', class_='item product_listbox oh')
    # print(products)
    for product in products:
        title = product.find('strong').text
        # print(title)
        price = product.find('div', class_='motive_box pull-right').find('strong').text
        # print(price)
        img ='https://www.kivano.kg/mobilnye-telefony' + product.find('img').get('src')
        # print(img)

        dict_ = {'title': title, 'price': price, 'img': img}
        write_to_csv(dict_)


with open('data_from_kivano.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title                                                  ', 'price                                         ', 'img'])


def main():
    url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='
    html = get_html(url)
    number = get_total_pages(html)
    # get_data(html)
    for i in range(2, number+1):
        url_with_page = url + pages + str(i)
        # print(url_with_page)
        html = get_html(url_with_page)
        get_data(html)
    Timer(60, main).start()

main()

