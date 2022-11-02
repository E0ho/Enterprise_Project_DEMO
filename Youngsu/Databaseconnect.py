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
import re


# STEP 2: MySQL Connection 연결
con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()

cur.execute("delete from platform_item")
con.commit()
# lists = [
        # "https://m.ycloset.com/"
#     # "https://m.mainbooth.co.kr/"
#     # "http://rimrim.co.kr",
#     # "https://themedicube.co.kr/",
#     # "https://www.andar.co.kr"
# ]

arr2 = []
num2 = cur.execute("SELECT * FROM html_url")
con.commit()
result = cur.fetchall()
for record in result:
    arr2.append(record)
    print(arr2[0][1])

# func1이 실행되면 cafe의 json을 가진 사이트를 파싱
def jsonParsing(list, k, app_key) : 
    try:
        requestdata = requests.get(f"https://{list}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}")
        return requestdata
    except:
        time.sleep(1)
        return htmlParsing()
    
   
# 모든 function이 실행되지 않으면 어쩔 수 없이 html 전체를 파싱해서 값을 가져오기(ex 메디큐브)
def htmlParsing() :
    # list를 일단 1개 받아서 num1으로 main에서 돌리기
    for i in range(num2):
        for k in range(180, 205):
        # 상품 판매 링크 가져오기
            header = {'User-Agent': 'Chrome/66.0.3359.181'}
            url_name = arr2[0][i]
            requestdata = requests.get(
                f"{url_name}/product/detail.html?product_no={k}", headers=header)

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
                    price = int(re.sub(r'[^0-9]', '', price))
                    print(price)

                    print('product_name :' + name, price)

                ##정규화해서 platform이름 넣어주기(hlist)
                cur.execute(f"INSERT INTO platform_item VALUES('{name}','{price}','{arr2[0][i]}')")
                con.commit()


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
arr1 = []
num1 = cur.execute("SELECT * FROM platform_input")
con.commit()
result = cur.fetchall()
for record in result:
    print(record)
    arr1.append(record)
    print(arr1[0][1])
##db에 있는 만큼 arr에 넣기 위해서 필요

#json parsing part
for i in range(num1) :
    for k in range(3000, 3011) :
        #위의 for문에 따라 parameter를 다르게 줘야함.
        platform = arr1[i][0]
        key = arr1[i][1]
        requestdata = jsonParsing(platform, k, key)
        # type으로 구분하는 걸로 바꿔야 할듯(json은 dict형태로 들어오기 때문에)
        # if type(requestdata)== dict :
        
        if requestdata.status_code == 200 :
            jsonData = requestdata.json()
            for data in jsonData :
                if jsonData.get(data).get("price") != None :

                    price :int = jsonData.get(data).get("price")
                    # code :int = jsonData.get(data).get("product_code")
                    # tax_free_price :int = jsonData.get(data).get("price_excluding_tax")
                    name :string = jsonData.get(data).get("product_name")
                    platform_name :string = arr1[i][0]
                    
                    str = f"INSERT IGNORE INTO platform_item VALUES('{name}','{price}','{platform_name}')"
                    cur.execute(str)
                    con.commit()
                    print(data, " : ", price, ", platform_name"," : ", platform_name)
                else :
                    continue
        else:
            continue

#html parsing part
htmlParsing()

con.close()