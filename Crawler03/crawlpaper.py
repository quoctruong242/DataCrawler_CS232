# Import necessary librarys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

# Access chromedriver
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options,
executable_path="C:/Users/TRUONG/Desktop/Crawler03/chromedriver.exe")
url = "https://vnexpress.net/"
driver.get(url)
time.sleep(3)

# Get link of post
elements = driver.find_elements_by_css_selector(".title-news>a")
storyTitles = [el.text for el in elements]
storyUrls = [el.get_attribute("href") for el in elements]

#print(storyTitles)
#print(storyUrls)
numpost = 1
list_dict = []
# Get info of post
for i in storyUrls[:numpost]:
    driver.get(i)
    elements = driver.find_elements_by_css_selector(".width_common")
    comment = [el.text for el in elements]
    # Get tittle, url, cmt of each post
    title = storyTitles[storyUrls.index(i)]
    url = storyUrls[storyUrls.index(i)]
    cmt = comment
    print(title)
    print(url)
    print(cmt)
"""
    dict_temp = {
        "title":title,
        "url": url,
        "cmt":cmt
    }
    list_dict.append(dict_temp)


data= {"post":list_dict}
json_string = json.dumps(data)
with open('json_data.json', 'w') as outfile:
    json.dump(json_string, outfile)
"""
