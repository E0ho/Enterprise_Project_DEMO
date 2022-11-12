#-*- coding: utf-8 -*-
# # api_list = [
# # # 패션
# # {'ozkiz' : 'ozkiz1'}, {'nerdy':'multinex'}, {'66girls':'mall66'},
# # {"spao":"spao"}, {"discovery": "discoveryglobal"}, {'stylenanado' : 'nandaglobal'},

# # # 뷰티
# # {"kundal" : "thesf1"},

# # # 푸드
# # {"mihsgnon": "nsmall2022"}, {"food-ology":"manfidence"}, {"healthhelper": "nextgoods"},

# # 가구
# {"curble":"abluestore"}, {"marketb":"marketb"}
# ]

import re

api_dict = {
    
# 패션
'ozkiz' : 'ozkiz1', 'nerdy':'multinex', '66girls':'mall66', "spao":"spao",
"discovery": "discoveryglobal", 'stylenanda' : 'nandaglobal', 'ggsing': "hkm0977", "leesle" : "leesle1",
"byther" : "harlem09", "pak-namae" : "piachess", "bluepops" : "ju021026", "habi-unni" : "mmmmj22", 
"giftxgift" : "kang24100", "monodaily" : "monodaily", "crump":"skw620", "athletekorea": "athlete", "monicaroom":"monica2012",
"mannergram":"s092814", "fibreno":"newfibreno", "jrium":"jrium917", "loar":"iroainc",
# 뷰티
"kundal":"thesf1", 
# 푸드
"mihsgnon": "nsmall2022", "food-ology":"manfidence", "healthhelper": "nextgoods","atemshop":"labnosh",
"labnosh":"labnosh", 
# 가구
"curble":"abluestore", "marketb":"marketb",

# 그 외
"chuu" : "chuukr", "ohscent" : "ohscent", "perfumegraphy": "pggraphy"

}

# print(len(api_dict))
# for i in api_list:
#     print(i)


import requests
import json
from bs4 import BeautifulSoup

# 해당 페이지의 Json 데이터를 파싱하는 함수
# url과 app_key를 함수의 파라미터로 사용하여 사용자로부터 전달 받는다.
def isAbleJson(shop_api_name, app_key):

    # shop_api_name 이 none 이면 json 파일이 존재하지 않기 때문에 html 파싱으로 이동.
    if shop_api_name != None:
        # 파싱하는 코드
        for k in range(129944, 129945):
            requestData = requests.get(f"https://{shop_api_name}.cafe24api.com/api/v2/products/{k}?shop_no=1&cafe24_app_key={app_key}")
            if requestData.status_code == 200:
                jsonParsing(requestData)
            else:
                continue

    else:
        print("html을 파싱하는 함수로 이동.")




def jsonParsing(requestData) : 
    # print(requestData.text)
    # print(type(requestData.text))
    
    jsonData = requestData.json()
    # print('==================================')
    print(jsonData)
    # print(type(jsonData))
    # print(jsonData.get('price'))

    html_list = ['description']
    # print(jsonData)
    print('=' * 170)
    for i in jsonData['product'].keys():
        if i in html_list:
            k = jsonData['product'].get(i)
            #print(k)

            header = {'User-Agent': 'Chrome/66.0.3359.181'}
            response = requests.get('https://66girls.co.kr//product/detail.html?product_no=129944', headers=header)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')
            # 사이트내 여러 선택사항
            #print(frame)

            select_list=[]
            
            for sel in frame.find_all('select'):
                select_list.append(sel)

            # 사이트 선택사항 갯수
            max = len(select_list)
            option_list = []
            
            # 선택사항마다의 옵션 추출
            for v in range(0, max):                
                for op in select_list[v].find_all('option'):
                    option_list.append([op.text])
            
            print(str(option_list))

            # html_text = '"""' + k + '"""'
            # with open('html_file.html', 'w', encoding='utf-8') as html_file:
            #     html_file.write(html_text)
            #print (type(k), k)
            # k = k.replace('\r\n', "")
            # print("달라진 k" , k)
            # result = re.sub(r'[^ ㄱ-ㅣ가-힣+]', '', k)
            # print('*' * 100)
            # print(result)

            #print(f"{i}의 대한 value값은 {jsonData['product'][i]}")
    

        # if i == 'detail_image' or i == 'tiny_image':
        #print(f"{i}의 대한 value 값 은 {jsonData['product'].get(i)}")
        
        # print("==================================")      
        # 
isAbleJson("mall66", "f7kOrfNK8UAn2Z93owrB4C")
#isAbleJson("ozkiz1", "KU5HdZg4BVXlfoLDEPu6EC")
#isAbleJson('marketb', 'O7Y0xDwkJRijRHPATmMJnC')

    