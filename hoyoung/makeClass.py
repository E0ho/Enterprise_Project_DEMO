class HTML :        
    
    header = {'User-Agent': 'Chrome/66.0.3359.181'}
    productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
    productPrice_List = ['#span_product_price_text' , 'li.price']
    productImg_List = ['.prdImg', '.imgArea','.product_image ','.thumbnail','.prd-image-list']
    parsing_list = [productName_List, productPrice_List, productImg_List]
    flag_index = []

    test_url_lists = [
        # "http://slowacid.com/",             #4000     ('table') - Class Name이 없는 경우 Table 구조를 띄고 있음 
        # "http://com-esta.co.kr/",           #450      (성공)
        # "https://monicaroom.com",           #14000    (성공)
        # "https://escstudio.kr",             # 600     ('table') - Class Name이 없는 경우 Table 구조를 띄고 있음 
        # "https://romand.co.kr",             # 500     (성공)
        "http://rimrim.co.kr",              # 150     (성공)
        # "https://m.mainbooth.co.kr/",       # 3015    (성공)
        # "https://m.ycloset.com/",           # 5300    (성공)
        # "https://www.unipopcorn.com",       # 1100    (성공)
        # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
        # "https://www.awesomeneeds.com"      # 2300    (성공)
    ]

    def find_value_from_HTML_atFirst(temp, index, flag, soup): 
        
        
        if not flag:
            frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')   

        # global wanted_value        
        if frame != None:
            if index < len(temp):  
                if frame.select_one(temp[index]) == None:
                    HTML.find_value_from_HTML_atFirst(temp , index + 1, flag, soup)
                else:
                    #wanted_value = return_value
                    #print(type(return_value))
                    #print(flag, index)
                    HTML.flag_index.append([flag, index])
                    return 
            else :       
                frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')
                if not flag and frame != None:
                    flag = True
                    HTML.find_value_from_HTML_atFirst(temp, 0, flag, soup)
        else : 
            return        

    def find_value_overOne(temp , flag, index, soup):
        
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

    def parsing_html(self):
        
        print(" 실행됩니다. ")

        start_loop_num = 150
        end_loop_num = 170
        count = 0
       

        for product_no in range(start_loop_num, end_loop_num):
            response = requests.get(
                f"{HTML.test_url_lists[0]}/product/detail.html?product_no={product_no}", headers=HTML.header)

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
                    for i in range(len(HTML.parsing_list)):              
                        # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)       
                        HTML.find_value_from_HTML_atFirst(HTML.parsing_list[i], 0, False, soup)    
                                    
                print(HTML.flag_index)
                for i in range(len(HTML.parsing_list)):    
                    if HTML.flag_index[i] != None:
                        wanted_value_list.append(HTML.find_value_overOne(HTML.parsing_list[i], HTML.flag_index[i][0], HTML.flag_index[i][1], soup))

                print(wanted_value_list)

    def option_parsing(self, product_no):  
        
        response = requests.get(f"https://66girls.co.kr//product/detail.html?product_no={product_no}", headers=HTML.header)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
        frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')      

        select_list=[]

        if frame == None:
            return None         
        else:
            for sel in frame.find_all('select'):            
                select_list.append(sel)

        # 사이트 선택사항 갯수
        max = len(select_list)
        option_list = []
        
        # 선택사항마다의 옵션 추출
        for v in range(0, max):                
            for op in select_list[v].find_all('option'):
                option_list.append([op.text])
        
        return option_list
        
import requests
from bs4 import BeautifulSoup

# html_parsing = HTML()
# html_parsing.parsing_html()