import requests
from bs4 import BeautifulSoup
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError


productName_List = ['.prd_name_wrap', '.prdnames', '.name', 'product_title' ]
productPrice_List = ['.font_Gilroy', '#span_product_price_text', '.price']
productImg_List = ['.imgArea', '.prdImgView', '.prdImg', '.img']

detail = [productImg_List, productPrice_List, productName_List]



url_list = [
    #"http://rimrim.co.kr"            # 150 ~ 200
    # "https://themedicube.co.kr/",     # 1 ~ 1200 # 상품명
    #"https://m.mainbooth.co.kr/",     # 3000 ~ 3200 # 이미지
    #"https://m.ycloset.com/",         # 5300 ~ 5500
    #"https://www.andar.co.kr"
    #"https://www.unipopcorn.com"   
    #"https://www.nothing-written.com"          # 6000 ~ 8000 # 상품명
    #"https://awesomeneeds.com"
]



def parsingData(temp , index): 
    
    global wanted_value

    if index < len(temp) :
        return_value = frame.select_one(temp[index])
        print(return_value)
        if return_value == None:
            parsingData(temp , index + 1)
        else:
            wanted_value = return_value
            return        
    else:
        if(type(temp[0]) != list):
            return "없는 클래스 이름입니다."
        else:
            temp = temp[index]
            parsingData(temp, 0)

for num1 in range(2300,2330):
        # 상품 판매 링크 가져오기
        header = {'User-Agent': 'Chrome/66.0.3359.181'}
        response = requests.get(
            f"{url_list[0]}/product/detail.html?product_no={num1}", headers=header)

        # 해당 url 존재 유무 파악
        if response.status_code == 200:
            # 파싱
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
            frame = soup.select_one('.InfoArea') if (soup.select_one('.InfoArea') != None) else soup.select_one('.detailArea')
            
            if frame == None:
                frame = soup.select_one('.product_info')    
            if frame != None:
                # 상품명, 가격, 이미지
                for i in range(len(detail)):
                    wanted_value = None
                    k = parsingData(detail[i], 0)
                    print(wanted_value)
                    if wanted_value != None:                        
                        if i == 0:                       
                            print (f"{i}번째 {wanted_value.select_one('img').get('src')}")
                        else:    
                            print(f"{i}번쨰 {wanted_value.text}")
            
                

