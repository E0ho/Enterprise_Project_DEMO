import re

url = "https://rimrim.com"
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
     

print(platform_name)