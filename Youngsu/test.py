from urllib import request
from email import header
import requests
from bs4 import BeautifulSoup
import json
import pymysql
import pyautogui
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError
import string
import time
import re

# lists = [
      # "https://m.ycloset.com/"
#     # "https://m.mainbooth.co.kr/"
#     # "http://rimrim.co.kr",
#     # "https://themedicube.co.kr/",
#     # "https://www.andar.co.kr"
# ]


# STEP 2: MySQL Connection 연결
con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                    db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()

cur.execute("delete from platform_item")
con.commit()

productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
productPrice_List = ['#span_product_price_text' , 'li.price']
productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

# 상품명 Parsing Class명 규칙 찾기
def select(name_num, price_num, img_num) :
    global frame


    # Product Name Class 찾기
    productName = frame.select_one(productName_List[name_num])
    while productName == None:
        name_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productName_List) <= name_num :
            productName = '예외 상황'
            name_num = 0
        else: productName = frame.select_one(productName_List[name_num])

    # Product Price Class 찾기
    productPrice = frame.select_one(productPrice_List[price_num])
    while productPrice == None:
        price_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productPrice_List) <= price_num :
            productPrice = 'sold out'
            price_num = 10000
        else: productPrice = frame.select_one(productPrice_List[price_num])

    # Product Img Class 찾기
    productImg = frame.select_one(productImg_List[img_num])
    while productImg == None:
        img_num += 1
        # 예외 처리 (오류 stop 방지 - None 사용)
        if len(productImg_List) <= img_num :
            productImg = '이미지 없음'
            img_num = 10000
        else: productImg = frame.select_one(productImg_List[img_num])
    
    # 해당 사이트 Class 조합 보여주기
    print(name_num, price_num, img_num)
    return name_num, price_num, img_num

def inputByUser():

    key = pyautogui.prompt("key 값을 입력해주세요..(없다면 None을 입력해주세요)")

    if key == "None" :
            url = pyautogui.prompt("url을 입력해주세요.")
            
            ##정규화해서 platform이름을 가져오기
            p = re.compile("www.\w+", re.MULTILINE)
            r = re.compile("//\w+", re.MULTILINE)

            platform_name = ""
            if not (p.findall(url)):
                platform_name = "".join(r.findall(url))
                platform_name = platform_name[2:]
                if platform_name == 'm':
                    p = re.compile("m.\w+", re.MULTILINE)
                    platform_name = "".join(p.findall(url))
                    platform_name = platform_name[2:]

            else:
                platform_name = "".join(p.findall(url))
                platform_name = platform_name[4:]
            
            cur.execute(f"INSERT INTO html_url VALUES('{url}','{platform_name}')")
            con.commit()
    else:
            header = pyautogui.prompt("json header를 입력해주세요..")
            cur.execute(f"INSERT INTO platform_input VALUES('{header}', '{key}')")
            con.commit()

def pullHtmlList():
    html_url_list = []
    count_html_list = cur.execute("SELECT * FROM html_url")
    con.commit()
    result = cur.fetchall()
    for record in result:
        html_url_list.append(record)
        print(html_url_list[0][0])
    
    htmlParsing(html_url_list, count_html_list)

def pullJsonList():
    json_url_list = []
    count_json_list = cur.execute("SELECT * FROM platform_input")
    con.commit()
    result = cur.fetchall()
    for record in result:
        print(record)
    json_url_list.append(record)
    print(json_url_list[0][1])
    jsonParsing(json_url_list, count_json_list)

##db에 있는 만큼 arr에 넣기 위해서 필요

# # func1이 실행되면 cafe의 json을 가진 사이트를 파싱
# def jsonParsing(list, k, app_key) : 
#     try:
#         requestdata = requests.get(f"https://{list}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}")
#         return requestdata
#     except:
#         time.sleep(1)
#         return htmlParsing()
    
   
# 모든 function이 실행되지 않으면 어쩔 수 없이 html 전체를 파싱해서 값을 가져오기(ex 메디큐브)
# def htmlParsing(html_url_list, count_html_list) :
#     # list를 일단 1개 받아서 num1으로 main에서 돌리기
#     for i in range(count_html_list):
#         for k in range(180, 205):
#         # 상품 판매 링크 가져오기
#             header = {'User-Agent': 'Chrome/66.0.3359.181'}
#             url_name = html_url_list[i][0]
#             requestdata = requests.get(
#                 f"{url_name}/product/detail.html?product_no={k}", headers=header)

#             # 해당 url 존재 유무 파악
#             if requestdata.status_code == 200:
#                 # 파싱
#                 html = requestdata.text
#                 soup = BeautifulSoup(html, 'html.parser')

#                 # 원하는 정보 추출
#                 name_tag = soup.select_one('.infoArea .prd_name_wrap')
#                 if name_tag == None :
#                     name_tag = soup.select_one('.infoArea .name')

#                 if name_tag == None :
#                     name_tag = soup.select_one('.xans-product-detail .prdnames')

#                 if name_tag == None :
#                     name_tag = soup.select_one('.xans-product-detail .name')


#                 price_tag = soup.select_one('.infoArea .font_Gilroy')
#                 if price_tag == None :
#                     price_tag = soup.select_one('.infoArea .price')
#                 if price_tag == None :
#                     price_tag = soup.select_one('#span_product_price_text')

#                 if price_tag != None and name_tag != None:
#                     name = name_tag.text
#                     price = price_tag.text
#                     price = re.sub(r'[^0-9]', '', price)
#                     # print(price)

#                     # print('product_name :' + name, price)

#                 ##정규화해서 platform이름 넣어주기(hlist)
#                 cur.execute(f"INSERT INTO platform_item VALUES('{name}','{price}','{html_url_list[0][i]}')")
#                 con.commit()
size_list=[]
color_list=[]
other_list=[]

def htmlParsing(html_url_list, count_html_list) :
    #list를 일단 1개 받아서 num1으로 main에서 돌리기
    for i in range(count_html_list):
        #DB에 저장되어 있는 html url 불러오기
        url_name = html_url_list[i][0]

        # 사이트마다 num 초기화
        name_num = 0
        price_num = 0
        img_num = 0
        a= None
        global frame
        

        # html 규칙 2 (주소/product/detail.html?product_no=(int)&cate_no=(int)&display_group=(int))
        for num1 in range(5300,15000):

            # 상품 판매 링크 가져오기
            header = {'User-Agent': 'Chrome/66.0.3359.181'}
            response = requests.get(f"{url_name}/product/detail.html?product_no={num1}", headers=header)

            # 해당 url 존재 유무 파악
            if response.status_code == 200:

                # 파싱
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                
                # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
                frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')

                # frame 안에서 infoarea접근하는 애들있고 , table, tbody, tr(1~2)
                # table = frame.find('table')
                # data = []
                # for tr in table.find_all('tr'):
                #     data.append(tr)
                # print(data[0].text)
                # print(data[1].text)

                # 판매 중단한 상품 거르기
                if frame != None :
                    
                # 우연히 첫 Select 함수 호출 때가 예외 사이트인 경우 (아주 드물게 사용)
                    # if a[0] == 10000 or a[1] == 10000 or a[2] == 10000 :
                    #     a = select(0,0,0)

                # Select함수에 한번만 접근하기 위한 if 문
                    if a == None:
                        print(num1)
                        a = select(name_num, price_num, img_num)
                        print(a)
                    
                    if frame.select_one(productName_List[a[0]]) == None:
                        name = '등록되지 않은 Class'
                    else :
                        name = frame.select_one(productName_List[a[0]]).text

                    # soldout 예외 처리
                    if frame.select_one(productPrice_List[a[1]]) == None :
                        price = 'sold out'
                    else :
                        price = frame.select_one(productPrice_List[a[1]]).text
                            
                    # 예외 상황에도 not Error
                    if frame.select_one(productImg_List[a[2]]) == None :
                        img = None
                    else:
                        imgDiv= frame.select_one(productImg_List[a[2]])
                        img = imgDiv.select_one('img').get('src')

                    # 사이트내 여러 선택사항
                    
                    
                    select_list=[]
                    for sel in frame.find_all('select'):
                        select_list.append(sel)

                    # 선택사항마다의 옵션 추출(모든 옵션 추출)
                    for v in range(0, len(select_list)):
                        option_list = []
                        print('옵션')
                        for op in select_list[v].find_all('option'):
                            option_list.append([op.text])
                        

                        item_list=[]
                        for i in range(2, len(option_list)):
                            
                            print(option_list[i][0])
                            
                            item_list.append(option_list[i][0])

                        #먼저 의류에서의 size, 색상을 구분해보자

                        
                        ##옵션이 ['- [필수] 옵션을 선택해 주세요 -'], ['-------------------'] 이것 외에 있을 경우 즉 옵션이 존재하는 경우를 예외처리
                        if(len(item_list)!=0):
                            
                            # print("haha",item_list[0])
                            # print("뭐냐",item_list)
                            #먼저 알파벳과 숫자만 출력(신발 사이즈 or M, L 와 같은 size)
                            #맨처음에 나오는 단어를 통해서 색상, size를 구분
                            size = re.compile('[a-zA-Z0-9]+').findall(item_list[0])
                            color = re.compile('[가-힣a-zA-Z]+').findall(item_list[0])
                            
                            print(str(size))
                            
                            # 의류, 신발
                            # 가정하기로는 size라는 언어가 나오거나 250과 길이가 0-3사이인 string이 들어오면(M,L,XL,XXL와 같은 것 포함) size로 판단
                            # 그리고 color의 경우에는 한글은 빨강, 영어는 red와 같이 2글자 이상이라고 생각해서 color를 판단
                            # 이상한 부품이나 엑세서리 옵션이 들어오는 경우는 예외처리가 어렵다.
                            #첫번째에서 size의 len을 측정하는 이유는 size에 아무것도 안 들어가 있는 경우의 예외처리 그리고 or 뒤의 것은 모두 조건 처리 
                            if(len(size)>0 and (str(size[0]).lower().strip() == 'size' or str(size[0]).lower().strip() == 'one' or str(size[0]).lower().strip() =='free' or (len(size[0]) <=3 and len(size[0])>=0))) :
                                    print("size_list에 for문을 이용한 item_list append")
                                    for k in item_list:
                                        size_list.append(k)
                                    print(size_list)

                            elif(len(color)>0 and len(color[0])>=2):
                                print("color_lits에 for문을 이용한 item_list append")
                                for l in item_list:
                                    color_list.append(l)
                                print(color_list)
                            else:
                                print("아무 옵션으로 달아놓고 other_list에 넣어서 db에 저장")
                                for m in item_list:
                                    other_list.append(m)
                                print(other_list)

                    print(option_list)
                    
                    if not option_list:
                        continue
                    else:
                        optionstr = str(option_list)
                        optionstr = optionstr.replace("'", "%")

                    print(name , price , img, optionstr)
                    price = re.sub(r'[^0-9]', '', price)
                    print(name , price , img)
                    k = str(color_list).replace("'",' ')
                    r = str(size_list).replace("'"," ")
                    cur.execute(f"INSERT INTO platform_item VALUES('{name}','{price}','{url_name}','{r}','{k}','{None}','{img}')")
                    con.commit()

                    print('------------------------------------------------')


                

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


#json parsing part
def jsonParsing(json_url_list, count_json_list):
    for i in range (count_json_list) :
        for k in range(3500, 4350) :
            #위의 for문에 따라 parameter를 다르게 줘야함.
            platform = json_url_list[i][0]
            key = json_url_list[i][1]
            requestdata = requests.get(f"https://{platform}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={key}")
            # type으로 구분하는 걸로 바꿔야 할듯(json은 dict형태로 들어오기 때문에)
            # if type(requestdata)== dict :
            
            if requestdata.status_code == 200 :
                jsonData = requestdata.json()

                
                for data in jsonData :
                    #가격이 음수로 나오는 이상한 값도 존재하고 description이 none이면 안되는 경우가 있어서 조건을 걸어줌.
                    if float(jsonData.get(data).get("price") or 0) > 0 and jsonData.get(data).get("description") != None:

                        price :int = jsonData.get(data).get("price")
                        # code :int = jsonData.get(data).get("product_code")
                        # tax_free_price :int = jsonData.get(data).get("price_excluding_tax")
                        name :string = jsonData.get(data).get("product_name")
                        img_url :string = jsonData.get(data).get("detail_image")
                        # des :string= jsonData.get(data).get("description")
                        # option : string = jsonData.get(data).get("")
                        # option = re.compile('[0-9]+').findall(des)
                        # print(description)
                        if(json_url_list[0]!=0):
                            platform_name :string = json_url_list[i][0]
                        else:
                            continue

                        str = f"INSERT INTO platform_item VALUES('{name}','{price}','{platform_name}','{None}','{None}','{None}','{img_url}')"
                        cur.execute(str)
                        con.commit()
                        print("platform_name", " : ", platform_name , ',', data, " : ", price, ", platform_name"," : ", platform_name, "img_url"," : ", img_url)
                        print("-----------------------------------------------------------------------------")
                    else :
                        continue
            else:
                continue


## Main

print("DB 연결완료")
# inputByUser()
print("사용자 입력 완료")
pullHtmlList()
print("HTML 파싱 완료")
pullJsonList()
print("json 파싱 완료")

con.close()
