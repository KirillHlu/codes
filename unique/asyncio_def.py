import requests
from bs4 import BeautifulSoup
import asyncio

url = 'https://www.vidal.ru/drugs/products/p/rus-a'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
# print(soup.find('h1'))

async def task_one():
    await asyncio.sleep(2)
    for t in soup.find('tr'):
        print(t)
        await asyncio.sleep(0.6)
asyncio.run(task_one())
