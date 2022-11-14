class InputSaving:

    import pymysql
    import pyautogui
    import requests
    import re

    con = pymysql.connect(host='127.0.0.1', user='root', password='fouridiot1234',
                        db='Capstone', charset='utf8') # 한글처리 (charset = 'utf8')

    # STEP 3: Connection 으로부터 Cursor 생성
    cur = con.cursor()

    def inputByUser():
        key = InputSaving.pyautogui.prompt("key 값을 입력해주세요..(없다면 None을 입력해주세요)")

        if key == "None" :
                
                url = InputSaving.pyautogui.prompt("url을 입력해주세요.")
                
                ##정규화해서 platform이름을 가져오기
                p = InputSaving.re.compile("www.\w+", InputSaving.re.MULTILINE)
                r = InputSaving.re.compile("//\w+", InputSaving.re.MULTILINE)

                platform_name = ""
                if not (p.findall(url)):
                        platform_name = "".join(r.findall(url))
                        platform_name = platform_name[2:]
                if platform_name == 'm':
                        p = InputSaving.re.compile("m.\w+", InputSaving.re.MULTILINE)
                        platform_name = "".join(p.findall(url))
                        platform_name = platform_name[2:]

                else:
                        platform_name = "".join(p.findall(url))
                        platform_name = platform_name[4:]
                
                InputSaving.cur.execute(f"INSERT INTO html_url VALUES('{url}','{platform_name}')")
                InputSaving.con.commit()
                
        else:
                header = InputSaving.pyautogui.prompt("json header를 입력해주세요..")
                InputSaving.cur.execute(f"INSERT INTO platform_input VALUES('{header}', '{key}')")
                InputSaving.con.commit()                
              
    con.close()


