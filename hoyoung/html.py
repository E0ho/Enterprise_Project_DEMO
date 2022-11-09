class HTML :

    import requests
    from bs4 import BeautifulSoup

    header = None
    productName_List = ['h1.-font-ns', 'li.name', 'div.prdnames', 'h1.name', 'h2.info_name','h3.product-name','h2.product_title','h2']
    productPrice_List = ['#span_product_price_text' , 'li.price']
    productImg_List = ['.prdImg', '.imgArea','.product_image ','.thumbnail','.prd-image-list']

    parsing_list = [productName_List, productPrice_List, productImg_List]

    # 초기화
    def __init__(self):
       
        this.header = {'User-Agent': 'Chrome/66.0.3359.181'}
        frame = None
        
    
    test_url_lists = [
        # "http://slowacid.com/",             #4000     ('table') - Class Name이 없는 경우 Table 구조를 띄고 있음 
        # "http://com-esta.co.kr/",           #450      (성공)
        # "https://monicaroom.com",           #14000    (성공)
        # "https://escstudio.kr",             # 600     ('table') - Class Name이 없는 경우 Table 구조를 띄고 있음 
        # "https://romand.co.kr",             # 500     (성공)
        # "http://rimrim.co.kr",              # 150     (성공)
        # "https://m.mainbooth.co.kr/",       # 3015    (성공)
        # "https://m.ycloset.com/",           # 5300    (성공)
        # "https://www.unipopcorn.com",       # 1100    (성공)
        # "https://www.nothing-written.com",  # 1700    (가격 - Hidden되어 있다)
        # "https://www.awesomeneeds.com"      # 2300    (성공)
    ]

    def find_value_from_HTML_atFirst(temp , index): 
    
        global frame
        # global wanted_value
        
        # InfoArea 까지 들어가서 확인한 것인가
        flag = False

        if index < len(temp) :
            return_value = frame.select_one(temp[index])
            if return_value == None:
                find_value_from_HTML(temp , index + 1)
            else:
                #wanted_value = return_value
                #print(type(return_value))
                return (flag, index)
        else :
            frame = soup.select_one('.InfoArea') if (soup.select_one('.InfoArea') != None) else soup.select_one('.detailArea')
            flag = True
            find_value_from_HTML(temp, 0)        

    def find_value_overOne(temp , flag, index):
        
        value = None
        if flag == False:
            value = frame.select_one(temp[index]).select_one('img').get('src') 

        else : 
            value = frame.select_one(temp[index]).text

        # 값이 있으면 리턴하고 없다면 None 을 반환한다.            
        return value if value != None else None

    def parsing_html():
        
        start_loop_num = 6000
        end_loop_num = 6030
        
        for product_no in range(start_loop_num, end_loop_num):
            response = requests.get(
                f"{url_list[0]}/product/detail.html?product_no={product_no}", headers=header)

            # 해당 url 존재 유무 파악
            if response.status_code == 200:
            
                # 파싱
                html = response.text        
                soup = BeautifulSoup(html, 'html.parser')
                
                # 필수 정보 추출 (이미지, 상품명, 가격, 사이즈)
                frame = soup.select_one('html body .xans-element-.xans-product.xans-product-detail')
                
                # 원하는 값을 넣는 리스트
                wanted_value_list = []
               
                # infoArea 까지 들어갔는지와 몇번째 인덱스에서 찾았는지에 대한 리스트
                flag_index_list = []

                if frame != None:
                    
                    # 상품명, 가격, 이미지
                    for i in range(len(parsing_list)):

                        if(product_no == start_loop_num) :                        
                            flag_index_list.append(find_value_from_HTML(parsing_list[i], 0))                
                        
                        wanted_value.append(find_value_overOne(parsing_list[i], flag_index_list[i][0], flag_index_list[i][1]))


                    print(wanted_value_list)
                        # wanted_value = None
                        # if wanted_value != None:                        
                        #     if i != 2:              
                        #         # print(f"{i}번쨰 {wanted_value.text}", "들어갔어")
                        #         wanted_value_list.append(wanted_value.text)                                 
                        #     else:  
                        #         #print (f"{i}번째 {wanted_value.select_one('img').get('src')}")
                        #         wanted_value_list.append(wanted_value.select_one('img').get('src'))  
                            
