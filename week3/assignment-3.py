import urllib.request
import json
import csv

url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
htmlfile = urllib.request.urlopen(url)
content = htmlfile.read().decode('utf-8')

data = json.loads(content)

attraction = []
mrt = {}
for x in data['result']['results']:
    address = x['address'][x['address'].find('區')-2:x['address'].find('區')+1]
    pic = x['file'][0:x['file'].find('https:',1)]
    attraction.append([x['stitle'],address,x['longitude'],x['latitude'],pic])

    if x['MRT'] == None:
        continue
    elif x['MRT'] not in mrt.keys():
        mrt.update({x['MRT']:[x['stitle']]})
    else:
        mrt[x['MRT']].append(x['stitle'])

with open('attraction.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(attraction)

dict_to_csv ="\n".join([k+','+','.join(v) for k,v in mrt.items()]) 
with open('mrt.csv','w',newline='') as f:
    f.write(dict_to_csv)


# 要求二
import bs4
def getTime(url):
    request = urllib.request.Request(url,headers={
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    })
    with urllib.request.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")
    details =[item.get_text(strip=True) for item in root.find_all(class_="article-meta-value")]
    return details[3]

def getData(url):
    # 建立一個 Request 物件，附加 Request Headers 資訊
    request = urllib.request.Request(url,headers={
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    })
    with urllib.request.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # 解析原始碼
    root = bs4.BeautifulSoup(data, "html.parser")
    articles = root.find_all("div",class_="r-ent")
    for article in articles:
        # 文章標題 article.a.string
        # 推文數量 reply
        if article.span == None:
            reply = '0'
        else:
            reply = article.span.string
        # 發布時間 time
        articleLink = "https://www.ptt.cc"+article.a['href']
        time = getTime(articleLink)
        # 存成txt
        with open('movie.txt','a',newline='') as f:
            f.write(article.a.string+','+reply+','+time+'\n')

    nextLink = root.find("a",string="‹ 上頁")
    return nextLink['href']


pageURL = 'https://www.ptt.cc/bbs/movie/index.html'
for i in range(0,3):
    pageURL = 'https://www.ptt.cc'+getData(pageURL)
