#encoding:utf-8
import requests
import sqlite3
import bs4
import json
import time
import random
import json
import numpy as np
# list 转成Json格式数据
def listToJson(lst):
    
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json
def dicToJson(raw):
    str_json = json.dumps(raw)
    return str_json
#user_agent 集合
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
headers={'User-Agent':random.choice(USER_AGENTS)}
url = 'https://ffxiv.eorzeacollection.com/glamours/lalafell?filter%5BorderBy%5D=date&filter%5BdatePeriod%5D=any&filter%5Bgender%5D=any&filter%5Bserver%5D=any&search=&author=&filter%5Bclassification%5D=&filter%5Bstyle%5D=&filter%5Btheme%5D=&filter%5Bcolor%5D=&filter%5Brace%5D%5B%5D=lalafell&filter%5BminimumLvl%5D=1&filter%5BmaximumLvl%5D=90&filter%5BheadPiece%5D=&filter%5BbodyPiece%5D=&filter%5BhandsPiece%5D=&filter%5BlegsPiece%5D=&filter%5BfeetPiece%5D=&filter%5BweaponPiece%5D=&filter%5BoffhandPiece%5D=&filter%5BearringsPiece%5D=&filter%5BnecklacePiece%5D=&filter%5BbraceletsPiece%5D=&filter%5BringPiece%5D=&filter%5BfashionPiece%5D=&page='
i = 1
x = 410
con = sqlite3.connect('./lalafell.db')

def parseAndSave(rc):
  ic = rc.find_all(class_='c-glamour-grid-item')
  for item in ic:
    rr_url = item.find(class_='c-glamour-grid-item-link').get('href')
    rr = requests.get("https://ffxiv.eorzeacollection.com"+rr_url,headers=headers)
    rrc = bs4.BeautifulSoup(rr.content.decode("utf-8"),"lxml")
    iic = rrc.find_all(class_='u-inset s-glamour-details-gallery-entry s-glamour-details-gallery-image u-cover-image')
    for item in iic:
      rrr_url = item.get('src')
      file_name = rrr_url.split('/')[-1]
      content_type = 'image/' + file_name.split('.')[-1]
      print(file_name)
      pic = requests.get(rrr_url,headers=headers);
      con.execute("INSERT INTO chat_image (cid, height, width, size, content_type, filename, url, source_url, type)VALUES (?,?,?,?,?,?,?,?,?)",("-1",0,0,0,content_type,file_name,rrr_url,"https://ffxiv.eorzeacollection.com"+rr_url,'拉拉肥'))
      con.commit()
      with open(str(file_name),'wb') as f:
        f.write(pic.content)
    print(iic)

def getData(i,url,USER_AGENTS):
    print(i)
    urln = url + str(i)
    #print(urln)
    headers={'User-Agent':random.choice(USER_AGENTS)}
    try:
        response = requests.get(urln,headers=headers)
    except ConnectionError:
       print("connectionError:"+urln)
       getData(i,url,USER_AGENTS)
    else:
        status_code = response.status_code
        content = bs4.BeautifulSoup(response.content.decode("utf-8"),"lxml")
        if(status_code == 404): 
            print('404_')
        else:
            try:
                # todo
                parseAndSave(content)
            except AttributeError:
               print("AttributeError")
               getData(i,url,USER_AGENTS)
           
while i<=x:#x:#1132
    try:
        getData(i,url,USER_AGENTS)
    except Exception as e:
        getData(i,url,USER_AGENTS)
    else:
        i = i + 1
con.close()