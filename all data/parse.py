from bs4 import BeautifulSoup as BS
import json
import os

def mkdir(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

def save_path(code):
    if len(code) == 5:
        return 'db/card/' + code + '.json'
    return 'db/umamusume/' + code + '.json'

if __name__ == "__main__":
    pin = ['20%', '50%', '70%', '90%', ''] # 세침사 이벤트 확률

    with open('crawl.txt', 'r', encoding="UTF-8") as f:
        json_data = json.load(f, strict=False)

    mkdir('db/card')
    mkdir('db/umamusume')


    for code in json_data.keys():
        conversed = {} # 이벤트 이름 : {이벤트 내용}

        for li in json_data[code]:
            contents = {} # 선택지 이름 : {선택지 내용}
            name = ''
            for key in li.keys():
                if key == 'name':
                    name = li[key]
                    continue

                if (len(li[key])):
                    None
                    # 선택지가 없는 경우를 제외하고싶다면 continue  사용
                    # 선택지가 없는 경우도 포함하고싶다면 None      사용
                
                idx = 0
                for content in li[key]:
                    soup = BS(content, "html.parser")
                    selection = soup.find('div', {'class': 'word'}).text

                    # rewards : 보상 일람, 선택지 내용
                    try:
                        rewards = [ x.get_text() for x in soup.find('div', {'class': 'reward'}).find_all('div') ]
                    except:
                        rewards = ['not in database']
                    
                    # 세침사 이벤트일 경우 확률 표시
                    if name.find('세침') > -1:
                        rewards.append(pin[idx])
                        idx += 1

                    contents[selection] = '\n'.join(rewards)

                conversed[name] = contents

        with open(save_path(code), 'w', encoding='UTF-8') as f:
            json.dump(conversed, f, ensure_ascii=False)