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

filename = "partition.txt"
f = open(filename, "w")
i = 1

def format2qlist(var, value):
  qlistline = "0" + " " + var + str(i) + " " + str(value) + ";"
  print(qlistline)
  f.write(qlistline + "\n")

def dataloop(soupsource, var, tag):
  global i
  tag.append("")
  for data in soupsource:
    l1 = data.findAll(tag[0], tag[1])
    for l2 in l1:
      format2qlist(var, l2.text.strip())
      i = i + 1

tag1 = ["span",{"class":"temp"}]
tag2 = ["td"]

dataloop(maxtemprow, "seq", tag1)
dataloop(mintemprow, "seq", tag1)
dataloop(humidity, "hum", tag2)

f.close()
print ("check")


