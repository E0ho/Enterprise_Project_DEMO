import HTMLClass as h
import JsonClass as j
import InputSavingClass as isc

pHTML = h.ParsingHTML()
pJson = j.ParsingJson()

pHTML.connectDB()
pJson.connectDB()
## 사용할 것 인가
# data1, data2 = isc.InputSaving()
