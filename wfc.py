import ssl
import urllib.request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
#from selenium import webdriver

ssl._create_default_https_context = ssl._create_unverified_context

#driver = webdriver.PhantomJS()
#url = 'https://weather.com/weather/tenday/l/Copenhagen+Denmark+DAXX0009:1:DA'
#url = 'https://www.wunderground.com/dk/copenhagen'
url = 'http://www.weather-forecast.com/locations/Copenhagen/forecasts/latest'

#driver.get(url)

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#soup = BeautifulSoup(driver.page_source, "lxml")

soup = BeautifulSoup(page_html, "html.parser")

temperatures = soup.find_all("span",{'class':"temp"})
maxtemprow = soup.find_all("tr",{"class":"max-temp-row"})


for temps in maxtemprow:
  maxtemp = temps.findAll("span",{"class":"temp"})
  print (maxtemp)


print ("check")


