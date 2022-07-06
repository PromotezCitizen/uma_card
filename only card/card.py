import requests
from bs4 import BeautifulSoup as BS
import json
import re
import os

def mkdir(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

def stringSplit(str):
    regexp = "[\t\n]"
    lst = list(filter(None, re.split(regexp, str.strip())))
    if ('또는' in lst): lst = sorted(set(lst), key = lambda x: lst.index(x)) # '또는' 키워드가 있을 경우 중복된 내용 제거
    return '\n'.join(lst)

def cardCrawling(id, name):
    path = 'card/' + id + '.json'
    if (os.path.isfile(path)):
        print('\t' + name + ' already exist')
        return

    print('\t' + name + ' crawling start!')
    url = 'https://uma.inven.co.kr/db/scard/' + id
    response = requests.get(url)
    soup = BS(response.text, "html.parser")

    card_events = {}
    for event in soup.find('dl', {'id': 'eventList'}).find_all('dl', {'class': 'event'}):
        if (event.find_all('dd').__sizeof__() < 120):
            continue
            # 선택지가 없는 경우를 제외하고싶다면 continue  사용
            # 선택지가 없는 경우도 포함하고싶다면 None      사용

        reward_list = {}

        for event_option in event.find_all('dd'):
            reward_list[event_option.find('div', {'class': 'eventWord'}).text] = \
                stringSplit(event_option.find('div', {'class': 'eventReward'}).text)

            # print(event_option.find('div', {'class': 'eventWord'}).text, \
            #     reward_list[event_option.find('div', {'class': 'eventWord'}).text], '\n\n\n')

        card_events[event.find('dt', {'class': 'eventName'}).text] = reward_list

    with open(path, 'w', encoding='UTF-8') as f:
        json.dump(card_events, f, ensure_ascii=False)

    print('\t' + name + ' crawling end!')

'''
# def __cardCrolling(path):
#     url = 'https://uma.inven.co.kr/db/scard/' + path
#     response = requests.get(url)
#     soup = BS(response.text, "html.parser")

#     eventList = soup.find('dl', {'id': 'eventList'}).find_all('dl', {'class': 'event'})

#     eventValue = {}
#     for dl in eventList:
#         rewardList = {}
#         for option in dl.find_all('dd', {'class': 'eventContent'}):
#             rewardTextList = []
#             for reward in option.find('div', {'class': 'eventReward'}):
#                 if (reward.find('div')) == -1:
#                     continue
#                 rewardTextList.append(reward.find('div').text.strip())

#             rewardList[option.find('div', {'class': 'eventWord'}).text] = '\n'.join(rewardTextList)

#         eventValue[dl.find('dt', {'class': 'eventName'}).text] = rewardList

#     filePath = 'card/' + id + '.json'
#     with open(filePath, 'w', encoding='UTF-8') as f:
#         json.dump(eventValue, f, ensure_ascii=False)
'''

def start():
    url = 'https://uma.inven.co.kr/db/scard/'
    response = requests.get(url)
    soup = BS(response.text, "html.parser")

    item = {}

    for card_list in soup.find('table', {'class': 'list_table'}).find('tbody'):
        item[card_list.find('a')['href'].split('/')[-1]] = card_list.find('span', {'class': 'charactername'}).text

    mkdir('card')

    with open('card/id_name.json', 'w', encoding='UTF-8') as f:
        json.dump(item, f,  ensure_ascii=False)

    for id, name in item.items():
        cardCrawling(id, name)

if __name__ == '__main__':
    print('crawling start!')
    start()
    print('crawling end!')