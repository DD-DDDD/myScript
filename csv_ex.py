import csv
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bs0bj = BeautifulSoup(html, 'lxml')
table = bs0bj.findAll("table", {'class': 'wikitable'})[0]
# 寻找表格的位置
rows = table.findAll('tr')
# tr代表每一行

csvFile = open("C:/Users/ricaito/Desktop/test/editors.csv", 'wt', newline='\n',
               encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
            writer.writerow(csvRow)
finally:
    csvFile.close()
