# Import the necessary library
import requests
from bs4 import BeautifulSoup
import csv

# url of webside to be needed crawl
name = "Thanh Duc Ngo"
root ="https://dl.acm.org"
# url after import keyword into search bar.
url = "https://dl.acm.org/action/doSearch?AllField=Ngo+Duc+Thanh"
page = 1

# Sent request to url with this page
r = requests.get(url.format(page))
print('status_code', r.status_code)

# Beautify file lxml by beautifulsoup library
soup = BeautifulSoup(r.content, 'lxml')

# Get block contain all page
def get_pages():
    list_pages =[]
    pages = soup.select_one("ul.rlist--inline.pagination__list")
    for i in pages:
        b1 = i.select_one("a", href=True)
        list_pages.append(b1["href"])
    return list_pages

list_pages = get_pages()

####### Check true author be needed search
def check_text(item, name):
    list_names = []
    b2 = item.select_one('ul.rlist--inline.loa.truncate-list')
    for i in b2:
        b3 = i.select_one("a > span").text
        list_names.append(str(b3))

    if name in list_names:
        return True
    else:
        return False


######## Get the name of author
def Author(item, name):
    list_names = []
    try:
        b2 = item.select_one('ul.rlist--inline.loa.truncate-list')
        for i in b2:
            b3 = i.select_one("a > span").text
            list_names.append(str(b3))
    except:
        print("Something else went wrong")
    return list_names

######### Get link paper and name of author
def get_link_author(all_items, name):
    list_link = []
    list_author = []
    for item in all_items:
        if check_text(item,name):
            part = item.select_one('span.hlFld-Title > a', href = True)
            list_link.append(root + part['href'])
            b2 = item.select_one('ul.rlist--inline.loa.truncate-list')
            temp =[]
            for i in b2:
                b3 = i.select_one("a > span").text
                temp.append(str(b3))
            list_author.append(temp)
    return list_link, list_author
"""
######## TO EXPERIMENT
# Lấy block cha chứa tất cả item trả về khi search
block_items = soup.select_one("ul.search-result__xsl-body.items-results.rlist--inline")

# Lấy các item trong bock b1
all_items = block_items.select("li.search__item.issue-item-container")
list_link, list_author = get_link_author(all_items,name)
print(list_link, list_author)"""


######### Get infomation of each paper of determined author
def get_info(url):
    #list_info = []
    r = requests.get(url.format(page))
    soup1 = BeautifulSoup(r.content, 'lxml')
    ######## Lấy title của bài báo
    Title = soup1.select_one("h1.citation__title").text
    #list_info.append(Title)

    ######## Lấy thời gian, sự kiện
    Time = soup1.select_one("span.dot-separator").text
    #list_info.append(Time)
    Event = soup1.select_one("span.epub-section__title").text
    #list_info.append(Event)

    ####### Lấy abstraction của paper
    Abstract = soup1.select_one("div.abstractSection.abstractInFull > p").text
    #list_info.append(Abstract)

    return Title, Time, Event, Abstract


data = []
"""
### TO EXPERIMENT
list_link = []
r = requests.get(list_pages[1].format(page))
print('status_code', r.status_code)
soup = BeautifulSoup(r.content, 'lxml')
# Lấy block cha chứa tất cả item trả về khi search
block_items = soup.select_one("ul.search-result__xsl-body.items-results.rlist--inline")

# Lấy các item trong bock b1
all_items = block_items.select("li.search__item.issue-item-container")
list_link, list_author = get_link_author(all_items,name)

count = 0
for link in list_link:
    templist = []
    Title, Time, Event, Abstract = get_info(link)
    templist = [Title, list_author[count], Time, Event, Abstract ]
    count +=1
    data.append(templist)

"""
######### MAIN
for i in list_pages:
    list_link = []
    r = requests.get(i.format(page))
    print('status_code', r.status_code)
    soup = BeautifulSoup(r.content, 'lxml')

    # Get result parent blocks contain all item
    block_items = soup.select_one("ul.search-result__xsl-body.items-results.rlist--inline")

    # Get each item in block1
    all_items = block_items.select("li.search__item.issue-item-container")
    list_link, list_author = get_link_author(all_items,name)
    if not list_link:
        break
    count = 0
    for link in list_link:
        Title, Time, Event, Abstract = get_info(link)
        templist = [Title, list_author[count], Time, Event, Abstract ]
        count +=1
        data.append(templist)

header = ["Title","Author","Time","Event","Abstract"]

######### Write output into csv file. We can try more concepts, such as my SQL, json file,...
with open('Crawler_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(data)
