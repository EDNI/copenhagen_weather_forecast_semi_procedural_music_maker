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

temperatures = soup.find_all("span",{'class':"temp"})
maxtemprow = soup.find_all("tr",{"class":"max-temp-row"})


for temps in maxtemprow:
  maxtemp = temps.findAll("span",{"class":"temp"})
  print (maxtemp)


print ("check")


