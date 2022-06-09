import requests
from bs4 import BeautifulSoup
import csv
import time

url = 'https://climatescape.org/organizations'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def get_html(url):
    src = requests.get(url, headers=headers)
    return src.text

def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    containers = soup.find_all('div', class_='border-gray-400 border-b flex text-gray-900 relative')
    links = []
    for container in containers:
        link = container.find('a', class_='flex flex-grow py-2 sm:py-4 sm:pl-2 sm:pr-16 hover:bg-gray-200').get('href')
        link = 'https://climatescape.org/' + link
        links.append(link)
    return links

def get_data(links):
    data_list = []
    count = 0
    for link in links:
        src_l = get_html(link)
        soup_l = BeautifulSoup(src_l, 'lxml')
        company = soup_l.find('div', class_='mr-2').find('h1', class_='flex-grow text-xl font-semibold').text
        try:
            about = soup_l.find('div', class_='mr-2').find('p').text
        except:
            about = 'Нет данных'
        try:
            description = soup_l.find('div', class_='my-6').text
        except:
            description = 'Нет данных'

        block_1 = soup_l.find('div', class_='flex flex-col mb-8').find('ul').find_all('li')[-1]

        try:
            employees = block_1.find('span').text
            employees = employees.split(' ')
            employees = employees[0]
        except:
            employees = 'Нет данных'

        block_2 = soup_l.find_all('div', class_='flex flex-col mb-8')
        block_2 = block_2[-2].find('ul').find_all('li')
        try:
            homepage = block_2[0].find('a').get('href')
        except:
            homepage = 'Нет данных'
        try:
            crunchbase = block_2[1].find('a').get('href')
        except:
            crunchbase = 'Нет данных'
        try:
            linkedin = block_2[2].find('a').get('href')
        except:
            linkedin = 'Нет данных'
        try:
            facebook = block_2[4].find('a').get('href')
        except:
            facebook = 'Нет данных'
        try:
            twitter = block_2[3].find('a').get('href')
        except:
            twitter = 'Нет данных'

        data_list.append(
            {
                'Link': link,
                'Company': company,
                'About': about,
                'Description': description,
                'Employees': employees,
                'Homepage': homepage,
                'Crunchbase': crunchbase,
                'LinkedIn': linkedin,
                'Facebook': facebook,
                'Twitter': twitter
            }
        )



        with open('climat.csv', 'a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                link,
                company,
                about,
                description,
                employees,
                homepage,
                crunchbase,
                linkedin,
                facebook,
                twitter
                )
            )
        count += 1
        print(f'stranica{count}')
        time.sleep(2)

def main():
    with open('climat.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Link',
                'Company',
                'About',
                'Description',
                'Employees',
                'Homepage',
                'Crunchbase',
                'LinkedIn',
                'Facebook',
                'Twitter'
            )
        )
    get_data(get_page(get_html(url)))

if __name__ == '__main__':
    main()