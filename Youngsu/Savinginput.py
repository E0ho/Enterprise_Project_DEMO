import pymysql
import pyautogui
import requests
import re

con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                       db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

# STEP 3: Connection 으로부터 Cursor 생성
cur = con.cursor()


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

con.close()

#만약 하나씩 저장할 때는 아래와 같이 코드 작성
#해당 값을 db에 한번만 저장하기 위해 사용
        # if not flag:
        #     str2= f"INSERT INTO platform_input VALUES('{platform}', '{key}')"
        #     cur.execute(str2)
        #     con.commit()
        #     flag = True

