from urllib import request
import requests
from bs4 import BeautifulSoup
import json
import pymysql
import pyautogui
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError
import string
import time
import signal


# STEP 2: MySQL Connection 연결
con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()

lists = [
    "https://m.ycloset.com/"
    # "https://m.mainbooth.co.kr/"
    # "http://rimrim.co.kr",
    # "https://themedicube.co.kr/",
    # "https://www.andar.co.kr"
]

# func1이 실행되면 cafe의 json을 가진 사이트를 파싱
def func1(list, k, app_key) : 
        # print(requestdata.status_code)
        # 실제 있는 사이트인지 확인하는 과정이 있어야 할 것 같다.
        # timeout전에 되면 json이 있는 것이고 없으면 html로 넘어가게 한다.
        
    try :
        requestdata = requests.get(f"https://{list}.cafe24api.com/api/v2/products/{k}?cafe24_app_key={app_key}")
        if requestdata.status_code==200 :
            print('fun1')
            req = requestdata.json()
            return req
    
    except :
        #delay를 안주게 되면 오류가 발생(대량의 request때문에 발생하는 것 같다.)
        time.sleep(1)
        return func2()
   
# 모든 function이 실행되지 않으면 어쩔 수 없이 html 전체를 파싱해서 값을 가져오기(ex 메디큐브)
def func2() :
    print('fun2')
    # list를 일단 1개 받아서 num1으로 main에서 돌리기
    for hlist in lists:
        for k in range(5300, 5500):
        # 상품 판매 링크 가져오기
            header = {'User-Agent': 'Chrome/66.0.3359.181'}
            requestdata = requests.get(
                f"{hlist}/product/detail.html?product_no={k}", headers=header)
            # 해당 url 존재 유무 파악
            if requestdata.status_code == 200:
                # 파싱
                html = requestdata.text
                soup = BeautifulSoup(html, 'html.parser')

                # 원하는 정보 추출
                name_tag = soup.select_one('.infoArea .prd_name_wrap')
                if name_tag == None :
                    name_tag = soup.select_one('.infoArea .name')

                if name_tag == None :
                    name_tag = soup.select_one('.xans-product-detail .prdnames')

                if name_tag == None :
                    name_tag = soup.select_one('.xans-product-detail .name')


                price_tag = soup.select_one('.infoArea .font_Gilroy')
                if price_tag == None :
                    price_tag = soup.select_one('.infoArea .price')
                if price_tag == None :
                    price_tag = soup.select_one('#span_product_price_text')

                if price_tag != None and name_tag != None:
                    name = name_tag.text
                    price = price_tag.text

                    print('product_name :' + name, price)

                return name, price

    

# python은 인터프리터 언어이기 때문에 순서를 잘 생각해야 한다.

# arr = [['ozkiz1', 'KU5HdZg4BVXlfoLDEPu6EC'],['mall66','f7kOrfNK8UAn2Z93owrB4C'],['marketb','O7Y0xDwkJRijRHPATmMJnC']]  #DB에서 불러와야함 (DICTIONARY 형태로)

#platform이름하고 api-key값만 받아서 변수로 저장해서
# key = pyautogui.prompt("key 값을 입력해주세요..")
# platform = pyautogui.prompt("json header를 입력해주세요..")

# flag = False
#입력받은 값을 DB에 저장

#list 형태로 가져와서 돌려보자

#원하는 만큼 돌리기

#list형태로 DB에서 받아와서 돌려보자
##두개 짝을 지어서 밑의 for문에 넣어줘야 할 듯
lists1 = cur.execute("SELECT platform_name FROM platform_input")
con.commit()
print(cur.fetchall())
##결과 (('mall66',), ('ozkiz1',))
lists2 = cur.execute("SELECT key_api FROM platform_input")
con.commit()
print(cur.fetchall())
##결과 (('f7kOrfNK8UAn2Z93owrB4C',), ('KU5HdZg4BVXlfoLDEPu6EC',))     

for platform in lists2:
    for k in range(5300, 5500) :

        #위의 for문에 따라 parameter를 다르게 줘야함.
        requestdata = func1(platform, k, key)

        # type으로 구분하는 걸로 바꿔야 할듯(json은 dict형태로 들어오기 때문에)
        if type(requestdata)== dict :
        
            #jsonData = requestdata.json()
            for data in requestdata :
                
                if requestdata.get(data).get("price") != None :

                    price :int = requestdata.get(data).get("price")
                    code :int = requestdata.get(data).get("product_code")
                    tax_free_price :int = requestdata.get(data).get("price_excluding_tax")
                    name :string = requestdata.get(data).get("product_name")
                    platform_name :string = platform

                    str = f"INSERT IGNORE INTO platform_item VALUES('{name}', '{code}' ,'{price}','{tax_free_price}','{platform_name}')"

                    cur.execute(str)

                    con.commit()

                    print(data, " : ", price, ", product_code", " : ", code)
                
                else :
                    continue

        #근데 이렇게 만들면 func2가 너무 여러번 돌아서 값이 이상하게 나옴...
        #func2 내부에서도 for문으로 돌고 위에서도 for문으로 돌아서 이상함.
        else:      
            func2()
con.close()