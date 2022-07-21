from operator import contains
import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import  urljoin
import json
from random import seed
from random import randint
# seed(1)
urls = []
nextUrls = []
totalUrls = []
thread_count = 1
indicator = 0
totalCount = 0

def isExistUrl(url):
    for link in totalUrls:
        if (url == link):
            return 0
    return 1

def isWikiUrl(url):
    slashCount = 0
    for count in range(len(url)) :
        if(slashCount == 3) :
            break
        if(url[count] == '/') :
            slashCount += 1
    localString = url[0 : count]
    if("wikipedia" in localString) :
        return 1
    return 0

def fetchLinks(url):
    global urls, nextUrls, totalCount, limit
    currentIndex = 0
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    for link in soup.find_all('a'):
        if(currentIndex > limit) :
            break
        str = urljoin(url, link.get('href'))
        totalCount += 1
        currentIndex += 1
        if isExistUrl(str) and isWikiUrl(str):
            nextUrls.append(str)
            totalUrls.append(str)
            print(str)


thread_count = randint(0, 20)
limit = randint(3, 4)
print(thread_count, limit)
url = 'https://www.wikipedia.org/'

fetchLinks(url)
urls = nextUrls
nextUrls = []
for cycle in range(thread_count - 1) :
    while indicator < len(urls):
        url = urls[indicator]
        indicator += 1
        fetchLinks(url)
    urls = nextUrls
    nextUrls = []
    indicator = 0

dictionary = {
	"totalCount": totalCount,
	"UniqueCount": len(totalUrls),
	"deep": thread_count,
	"limitEachPage": limit,
    "data": totalUrls
}
 
with open("result.json", "w") as outfile:
    json.dump(dictionary, outfile)
# threads = []
# for i in range(thread_count):
#     thread = threading.Thread(target=thread_task)
#     thread.start()
#     threads.append(thread)

# for i in range(thread_count):
#     threads[i].join()

