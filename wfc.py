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
daynumb = int(soup.find("div", {"class":"dom"}).text.strip())

perdic = {"AM": 0, "PM": 1, "Night" : 2}

pertemp = perdic[periodstart]

maxam=[]
minam=[]
maxpm=[]
minpm=[]
maxnt=[]
minnt=[]
maxs=[maxam,maxpm,maxnt]
mins=[minam,minpm,minnt]
hums=[[]]
decaseq = [0,0,0,0,0,0,0,0,0,0]

filename = "partition.txt"
f = open(filename, "w")
i = 1

def format2qlist(var, value):
  qlistline = "0 " + var + str(i) + " " + str(value) + ";"
#  print(qlistline)
  f.write(qlistline + "\n")

def dataloop(soupsource, var, tag, datalist, dln):
  global pertemp
  tag.append("")
  for data in soupsource:
    l1 = data.findAll(tag[0], tag[1])
    for l2 in l1:
      datalist[pertemp % dln].append(l2.text.strip())
      pertemp += 1

def decaseqmaker(datalist1=[], datalist2=[]):
  sourcelist=[datalist1,datalist2]
  j = 0
  while j < 10:
    decaseq[j]=sourcelist[0][int(j/2)]
    decaseq[j+1]=sourcelist[1][int(j/2)]
    j += 2

temptag = ["span",{"class":"temp"}]
humtag = ["td"]

dataloop(maxtemprow, "seq", temptag, maxs, 3)
dataloop(mintemprow, "seq", temptag, mins, 3)
dataloop(humidity, "hum", humtag, hums, 1)

##########DEFAULT#####SETTINGS##############################

#global cm1s, cm2s, cm3s, cm4s

cm1s = [2,3,6,7, "cm1s"]
cm2s = [3,4,5,0, "cm2s"]
cm3s = [0,0,0,0, "cm3s"]
cm4s = [0,0,0,0, "cm4s"]

#global pnba, pnbb, pnbc, pnbd

pnba = [3,4,25, "pnba"]
pnbb = [4,6,25, "pnbb"]
pnbc = [3,25,25, "pnbc"]
pnbd = [2,25,25, "pnbd"]

#global ppba, ppbb, ppbc, ppbd

ppba = [8,25,25, "ppba"]
ppbb = [12,25,25, "ppbb"]
ppbc = [6,25,25, "ppbc" ]
ppbd = [4,25,25, "ppbd" ]

#global pwba, pwbb, pwbc, pwbd

pwba = [7,25,25, "pwba" ]
pwbb = [10,25,25, "pwbb" ]
pwbc = [5,25,25, "pwbc" ]
pwbd = [7,25,25, "pwbd" ]


#global ppqtset, pEDOset
ppqtset = [0,0,3,3,3,6,6,6,8,8,10,11,12,13,14,15,16,17,18,19]
pEDOset = 10

#global seqcpt1, 
seqcpt1 = minnt
seqcpt2 = maxpm

bpm = daynumb * 2 + 70
seql = 10

###########################################################

########################MOD################################
modslist = ["Mornings (type 'm')", "Chaos (type 'c')"]

def m1mod():
  seqcpt1 = minam
  seqcpt2 = maxam
  print("m1mod done")

def chmod():
  cm1s = [2,3,6,7, "cm1s"]
  cm2s = [3,4,5,0, "cm2s"]
  cm3s = [4,5,7,8, "cm3s"]
  cm4s = [2,3,5,7, "cm4s"]
  pnba = [20,25,25, "pnba"]
  pnbb = [21,25,25, "pnbb"]
  pnbc = [22,25,25, "pnbc"]
  pnbd = [23,25,25, "pnbd"]
  ppba = [24,25,25, "ppba"]
  ppbb = [20,25,25, "ppbb"]
  ppbc = [21,25,25, "ppbc" ]
  ppbd = [22,25,25, "ppbd" ]
  pwba = [23,25,25, "pwba" ]
  pwbb = [24,25,25, "pwbb" ]
  pwbc = [20,25,25, "pwbc" ]
  pwbd = [21,25,25, "pwbd" ]
  print("chmod done")


#modsdic = {"m": m1mod, "c": chmod }
modsdic = {"m": m1mod, "c": chmod}

#altmodask = input("do you want to use other settings? Y / N ")

#if altmodask == 'Y':
#  print("these are the availble mods:")
#  print (modsdic)
#  print(modslist)
#  modselect = input("wich one do you want to try?")
#  print("let's go")
#  modtocall = modsdic[modselect]
#  modtocall()

##########################################################
decaseqmaker(seqcpt1, seqcpt2)
cmxs = [cm1s,cm2s,cm3s,cm4s]
pnpwbs = [pnba,pnbb,pnbc,pnbd,ppba,ppbb,ppbc,ppbd,pwba,pwbb,pwbc,pwbd]

i = 0
while i < 4:
  for shlurps in cmxs:
    format2qlist(shlurps[4],shlurps[i])
  i += 1

i = 0
while i < 3:
  for shlurps in pnpwbs:
    format2qlist(shlurps[3], shlurps[i])
  i += 1

i = 1
format2qlist("bpm", bpm)
format2qlist("seql", seql)

i = 0
while i < 10:
  format2qlist("dseq", decaseq[i])
  i += 1
i = 0

while i < 10:
  format2qlist("hum", hums[0][i])
  i += 1

i = 0
format2qlist("pEDOset",pEDOset)

while i < 20:
 format2qlist("ppqtset", ppqtset[i])
 i += 1

f.close()
