import requests
from bs4 import BeautifulSoup
import time
from email import header
from http.client import ImproperConnectionState
from urllib.error import URLError, HTTPError


productName_List = ['product-name','.prd_name_wrap', '.prdnames','.name','h2','h3','h1']
productPrice_List = ['.font_Gilroy', '#span_product_price_text', '.price']
productImg_List = ['.product_image ','.prdImgView', '.imgArea', '.prd-image-list']

name_list = [productName_List, productPrice_List, productImg_List]



url_list = [
    # "http://rimrim.co.kr"            # 150 ~ 200
    # "https://themedicube.co.kr/",     # 1 ~ 1200 # 상품명
    # "https://m.mainbooth.co.kr/",     # 3000 ~ 3200 # 이미지
    # "https://m.ycloset.com/",         # 5300 ~ 5500
    # "https://www.andar.co.kr"
    # "https://www.unipopcorn.com"   
    # "https://www.nothing-written.com"          # 6000 ~ 8000 # 상품명
    # "https://awesomeneeds.com"
]



def parsingData(temp , index): 
    
    global wanted_value

    if index < len(temp) :
        return_value = frame.select_one(temp[index])
        if return_value == None:
            parsingData(temp , index + 1)
        else:
            wanted_value = return_value
            return 
    else :
        print("파싱되는 데이터가 없습니다.")
        return        



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
            frame = soup.select_one('.xans-product-detail')
            if frame == None:
                frame = soup.select_one('.InfoArea') if (soup.select_one('.InfoArea') != None) else soup.select_one('.detailArea')
           
            if frame != None:
                # 상품명, 가격, 이미지
                for i in range(len(name_list)):
                    wanted_value = None
                    parsingData(name_list[i], 0)

                    wanted_value_list = []
                    if wanted_value != None:                        
                        if i == 2:                       
                            print (f"{i}번째 {wanted_value.select_one('img').get('src')}")
                            wanted_value_list.append(wanted_value.select_one('img').get('src'))
                        else:    
                            print(f"{i}번쨰 {wanted_value.text}")
                            wanted_value_list.append(wanted_value.text)
            
                

