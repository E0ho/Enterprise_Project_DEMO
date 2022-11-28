
class DBClass:

    import re
    import pymysql
    # 사이트내 여러 선택사항
    size_list=[]
    color_list=[]
    other_list=[]
    select_list=[]

    con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                    db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
    cur = con.cursor()

    def insert_data_to_DB(platformName, product_name, product_price, img, option_list):
        # 옵션리스트에 대해서 4가지 리스트에 대해 전처리 한다.
        DBClass.option_parsing(option_list)
        
        ## 리턴 되었을 때는 size, color, other, select 리스트에 채워져 있을 것.
        ## DB Attribute 순서는 잘모르겠습니당.

        size = " ".join(DBClass.size_list).replace("'", "%")
        color = " ".join(DBClass.color_list).replace("'", "%")
        other = " ".join(DBClass.other_list).replace("'", "%")
        # select = " ".join(DBClass.select_list)
        DBClass.cur.execute(f"INSERT INTO platform_item VALUES('{product_name}','{product_price}','{img}','{size}','{color}','{other}','{platformName}')")
        DBClass.con.commit()


    def option_parsing(option_list):
        item_list=[]
        for i in range(2, len(option_list)):
            
            print(option_list[i][0])
            
            item_list.append(option_list[i][0])

        #먼저 의류에서의 size, 색상을 구분해보자

        
        ##옵션이 ['- [필수] 옵션을 선택해 주세요 -'], ['-------------------'] 이것 외에 있을 경우 즉 옵션이 존재하는 경우를 예외처리
        if(len(item_list)!=0):
            
            print("haha",item_list[0])
            print("뭐냐",item_list)
            #먼저 알파벳과 숫자만 출력(신발 사이즈 or M, L 와 같은 size)
            #맨처음에 나오는 단어를 통해서 색상, size를 구분
            size = DBClass.re.compile('[a-zA-Z0-9]+').findall(item_list[0])
            color = DBClass.re.compile('[가-힣a-zA-Z]+').findall(item_list[0])
            
            print(str(size))
            
            # 의류, 신발
            # 가정하기로는 size라는 언어가 나오거나 250과 길이가 0-3사이인 string이 들어오면(M,L,XL,XXL와 같은 것 포함) size로 판단
            # 그리고 color의 경우에는 한글은 빨강, 영어는 red와 같이 2글자 이상이라고 생각해서 color를 판단
            # 이상한 부품이나 엑세서리 옵션이 들어오는 경우는 예외처리가 어렵다.
            #첫번째에서 size의 len을 측정하는 이유는 size에 아무것도 안 들어가 있는 경우의 예외처리 그리고 or 뒤의 것은 모두 조건 처리 
            if(len(size)>0 and (str(size[0]).lower().strip() == 'size' or str(size[0]).lower().strip() == 'one' or str(size[0]).lower().strip() =='free' or (len(size[0]) <=3 and len(size[0])>=0))) :
                    print("size_list에 for문을 이용한 item_list append")
                    for k in DBClass.item_list:
                        DBClass.size_list.append(k)
                    print(DBClass.size_list)

            elif(len(color)>0 and len(color[0])>=2):
                print("color_lits에 for문을 이용한 item_list append")
                for l in item_list:
                    DBClass.color_list.append(l)
                print(DBClass.color_list)
            else:
                print("아무 옵션으로 달아놓고 other_list에 넣어서 db에 저장")
                for m in item_list:
                    DBClass.other_list.append(m)
                print(DBClass.other_list)

  
