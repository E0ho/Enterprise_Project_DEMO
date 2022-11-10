import requests
from bs4 import BeautifulSoup
import time
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError

url_list = [
    "http://rimrim.co.kr"            # 150 ~ 200
    # "https://themedicube.co.kr/",     # 1 ~ 1200 # 상품명
    # "https://m.mainbooth.co.kr/",     # 3000 ~ 3200 # 이미지
    # "https://m.ycloset.com/",         # 5300 ~ 5500
    # "https://www.andar.co.kr"         # 6000
    # "https://www.unipopcorn.com"   
    # "https://www.nothing-written.com"          # 6000 ~ 8000 # 상품명
    # "https://awesomeneeds.com"
]


# for product_no in range(6000,6030):
#     # 상품 판매 링크 가져오기
#     header = {'User-Agent': 'Chrome/66.0.3359.181'}
#     response = requests.get(
#         f"{url_list[0]}/product/detail.html?product_no={product_no}", headers=header)

#     # 해당 url 존재 유무 파악
#     if response.status_code == 200:
#         # 파싱
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')

#         # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
#         frame = soup.select_one('.xans-product-detail')
#         wanted_value_list = []
#         option_list = []

#         if frame != None:
            
#             # 상품명, 가격, 이미지
#             for i in range(len(name_list)):
                
#                 wanted_value = None
#                 find_value_from_HTML_atFirst(name_list[i], 0)                
                
#                 if wanted_value != None:                        
#                     if i != 2:              
#                         # print(f"{i}번쨰 {wanted_value.text}", "들어갔어")
#                         wanted_value_list.append(wanted_value.text)                                 
#                     else:  
#                         #print (f"{i}번째 {wanted_value.select_one('img').get('src')}")
#                         wanted_value_list.append(wanted_value.select_one('img').get('src'))  
                        
            
#             select_list=[]
#             for sel in frame.find_all('select'):
#                 select_list.append(sel)

#             # 선택사항마다의 옵션 추출
#             for v in range(0, len(select_list)):
            
#                 for op in select_list[v].find_all('option'):
#                     option_list.append([op.text])
#         # 사이트내 여러 선택사항
        
#             #print(option_list)

#         print(option_list, wanted_value_list)



productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
productPrice_List = ['#span_product_price_text' , 'li.price']
productImg_List = ['.prdImg', '.imgArea','.product_image ','.thumbnail','.prd-image-list']

name_list = [productName_List, productPrice_List, productImg_List]

def find_value_from_HTML_atFirst(temp, index, flag): 
    
    global flag_index
    
    if not flag:
        frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')   

    # global wanted_value        
    if frame != None:
        if index < len(temp):  
            if frame.select_one(temp[index]) == None:
                find_value_from_HTML_atFirst(temp , index + 1, flag)
            else:
                #wanted_value = return_value
                #print(type(return_value))
                #print(flag, index)
                flag_index.append([flag, index])
                return 
        else :       
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail .infoArea')
            if not flag and frame != None:
                flag = True
                find_value_from_HTML_atFirst(temp, 0, flag)
    else : 
        return        

def find_value_overOne(temp , flag, index):
    
    value = None
    if not flag:
        frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')
        if frame.select_one(temp[index]).select_one('img') != None:
            value = frame.select_one(temp[index]).select_one('img').get('src')
            if value == None:
                value = frame.select_one(temp[index]).text
                
    else : 
        frame = soup.select_one('.infoArea') if (soup.select_one('.infoArea') != None) else soup.select_one('.detailArea')
        if frame != None:
            value = frame.select_one(temp[index]).text

    # 값이 있으면 리턴하고 없다면 None 을 반환한다.            
    return value if value != None else None


    
print(" 실행됩니다. ")

header = {'User-Agent': 'Chrome/66.0.3359.181'}

start_loop_num = 150
end_loop_num = 250

## 총 몇번 파싱되었는지
count = 0

# infoArea 까지 들어갔는지와 몇번째 인덱스에서 찾았는지에 대한 리스트
flag_index = []

for product_no in range(start_loop_num, end_loop_num):
    response = requests.get(
        f"{url_list[0]}/product/detail.html?product_no={product_no}", headers=header)

    # 해당 url 존재 유무 파악
    if response.status_code == 200:
    
        # 파싱
        html = response.text        
        soup = BeautifulSoup(html, 'html.parser')       

        # 원하는 값을 넣는 리스트
        wanted_value_list = []
 
        count += 1

        if count == 1 :
        # 상품명, 가격, 이미지
            for i in range(len(name_list)):              
                # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)       
                find_value_from_HTML_atFirst(name_list[i], 0, False)    
                             
        print(flag_index)
        for i in range(len(name_list)):    
            if flag_index[i] != None:
                wanted_value_list.append(find_value_overOne(name_list[i], flag_index[i][0], flag_index[i][1]))

        print(wanted_value_list)

