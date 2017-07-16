import ssl
import urllib.request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

url = 'http://www.weather-forecast.com/locations/Copenhagen/forecasts/latest'
uClient = uReq(url)
page_html = uClient.read()
uClient.close()
soup = BeautifulSoup(page_html, "html.parser")

maxtemprow = soup.findAll("tr",{"class":"max-temp-row"})
mintemprow = soup.findAll("tr",{"class":"min-temp-row"})
humidity = soup.findAll("tr",{"class":"rh"})
periodstart = soup.find("div",{"class":"pname"}).text.strip()
daynumb = soup.find("div", {"class":"dom"}).text.strip()

perdic = {"AM": 0, "PM": 1, "Night" : 2}

pertemp = perdic[periodstart]
print(daynumb)

maxam=[]
minam=[]
maxpm=[]
minpm=[]
maxnt=[]
minnt=[]
maxs=[maxam,maxpm,maxnt]
mins=[minam,minpm,minnt]
hums=[[]]
decaseq = []
filename = "partition.txt"
f = open(filename, "w")
i = 1

def format2qlist(var, value):
  qlistline = "0" + " " + var + str(i) + " " + str(value) + ";"
  print(qlistline)
  f.write(qlistline + "\n")

def dataloop(soupsource, var, tag, datalist, dln):
  global i
  global pertemp
  tag.append("")
  for data in soupsource:
    l1 = data.findAll(tag[0], tag[1])
    for l2 in l1:
      i = i + 1
      datalist[pertemp % dln].append(l2.text.strip())
      pertemp += 1

tag1 = ["span",{"class":"temp"}]
tag2 = ["td"]

dataloop(maxtemprow, "seq", tag1, maxs, 3)
dataloop(mintemprow, "seq", tag1, mins, 3)
dataloop(humidity, "hum", tag2, hums, 1)

mode = 0

if mode == 0:
  decaseq = [maxam[0],minnt[0],maxam[1],minnt[1],maxam[2],minnt[2],maxam[3],minnt[3],maxam[4],minnt[4]]
else:
  decaseq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


i = 0
while i < 10:
  format2qlist("dseq", decaseq[i])
  i += 1
i = 0
while i < 10:
  format2qlist("hum", hums[0][i])
  i += 1


f.close()

