import asyncio
from bs4 import BeautifulSoup
import aiohttp
import csv

url = 'https://climatescape.org/organizations'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

data_list = []

async def get_page_data(session, link):
    async with session.get(link, headers=headers) as response:
        response_text = await response.text()
        soup_l = BeautifulSoup(response_text, 'lxml')
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



async def gather_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        containers = soup.find_all('div', class_='border-gray-400 border-b flex text-gray-900 relative')
        tasks = []

        for container in containers:
            link = container.find('a', class_='flex flex-grow py-2 sm:py-4 sm:pl-2 sm:pr-16 hover:bg-gray-200').get(
                'href')
            link = 'https://climatescape.org' + link
            print(link)
            task = asyncio.create_task(get_page_data(session, link))

            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())
    with open('climat_1.csv', 'w') as file:
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

    for data in data_list:
        with open('climat_1.csv', 'a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                data['link'],
                data['company'],
                data['about'],
                data['description'],
                data['employees'],
                data['homepage'],
                data['crunchbase'],
                data['linkedin'],
                data['facebook'],
                data['twitter']
                )
            )

if __name__ == '__main__':
    main()