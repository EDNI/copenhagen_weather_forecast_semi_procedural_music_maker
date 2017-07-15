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

for temps in maxtemprow:
  maxtemp = temps.findAll("span",{"class":"temp"})
  for tempspan in maxtemp:
    format2qlist("seq", tempspan.text.strip()) 
    i = i + 2

i = 2
for temps in mintemprow:
  mintemp = temps.findAll("span",{"class":"temp"})
  for tempspan in mintemp:
    format2qlist("seq", tempspan.text.strip()) 
    i = i + 2

i = 0
for humhum in humidity:
  hum = humhum.findAll("td")
  for humtd in hum:
    format2qlist("hum", humtd.text.strip())
    i = i + 1


f.close()
print ("check")


