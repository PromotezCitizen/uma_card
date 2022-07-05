from bs4 import BeautifulSoup as BS
import json
import re

with open('crawl.txt', 'r', encoding="UTF-8") as f:
    json_data = json.load(f, strict=False)


conversed = {}
for li in json_data["102701"]:
    contents = {}
    for key in li.keys():
        if key == 'name':
            continue
        
        if (len(li[key])):
            None
            # 선택지가 없는 경우를 제외하고싶다면 continue  사용
            # 선택지가 없는 경우도 포함하고싶다면 None      사용

        for content in li[key]:
            soup = BS(content, "html.parser")

            selection = soup.find('div', {'class': 'word'}).text
            rewards = [ x.get_text() for x in soup.find('div', {'class': 'reward'}).find_all('div') ]

            contents[selection] = '\n'.join(rewards)

    print(contents)

