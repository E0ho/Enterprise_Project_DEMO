import string
import requests
import json
import pymysql
from bs4 import BeautifulSoup as bs


# STEP 2: MySQL Connection 연결
con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()





# func1이 실행되면 shop의 json을 가진 사이트를 파싱
def func1(list, k, app_key) :
    try:
        requestdata = requests.get(f"https://{list}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}&cafe24_api_version=2022-06-01")
        return requestdata
    except:
        return func2(list, k, app_key)      


# func2가 실행되면 cafe의 json을 가진 사이트를 파싱
def func2(list, k, app_key) : 
    try:
        requestdata = requests.get(f"https://{list}.cafe24api.com/api/v2/products/{k}?cafe24_app_key={app_key}")
        
        return requestdata
    except:
        return func3()

# 모든 function이 실행되지 않으면 어쩔 수 없이 html 전체를 파싱해서 값을 가져오기(ex 메디큐브)
def func3() :
    page = requests.get("https://themedicube.co.kr/product/detail.html?product_no=1103&cate_no=466&display_group=2")
    soup = bs(page.text, "html.parser")

    return soup


# rows = 2  # 2개의 사이트를 저장
# cols = 2  # 사이트의 json url의 이름과 api_key 값 저장(2개)
# arr = [[0 for i in range(cols)] for j in range(rows)]  # 예시 [url_name, api_key], [url_name, api_key], ....   ==> 나중에 여러 사이트를 돌릴때는 이렇게 하는게 좋을듯?


# python은 인터프리터 언어이기 때문에 순서를 잘 생각해야 한다.

arr = [['ozkiz1', 'KU5HdZg4BVXlfoLDEPu6EC'],['nsmall2022','KU5HdZg4BVXlfoLDEPu6EC']]  #DB에서 불러와야함 (DICTIONARY 형태로)

#일단 오즈킺즈의 3757과 농심의 3757이 겹치므로 두개만 해보겠다. + 메디큐브도 html이 파싱되는지 확인해보기  
# -> 메디큐브의 경우 mod_security 또는 다른 비슷한 서버 시큐리티가 알려진 사용자 봇을 블록 시키기 때문에 html파싱이 안된다..... 어떻게 해야 할까??

for i in range(0, 3) :
    for k in range(3758, 3760) :
        list = arr[i][0]
        app_key=arr[i][1]

        requestdata = func1(list, k, app_key)
        
        if requestdata.status_code == 200 :
            jsonData = requestdata.json()
            for data in jsonData :
                if jsonData.get(data).get("price") != None :
                    print(f"{arr[i][0]}의 {k}페이지 입니다.----------------------------------------------")
                    #일단 5가지만 mysql에 저장해보기
                   
                    price :int = jsonData.get(data).get("price")
                    code :int = jsonData.get(data).get("product_code")
                    tax_free_price :int = jsonData.get(data).get("price_excluding_tax")
                    name :string = jsonData.get(data).get("product_name")
                    platform_name :string = arr[i][0]

                    str = f"INSERT INTO platform_item VALUES('{name}', '{code}' ,'{price}','{tax_free_price}','{platform_name}')"

                    cur.execute(str)

                    con.commit()
                    con.close()

                    print(data, " : ", price, ", product_code", " : ", code)
                
                else :
                    continue

        else : 
            print(requestdata)
    con.close()