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

maxam, maxpm, maxnt = [],[],[]
minam, minpm, minnt = [],[],[]
#maxpm=[]
#minpm=[]
#maxnt=[]
#minnt=[]
maxs=[maxam,maxpm,maxnt]
mins=[minam,minpm,minnt]
hums=[[]]
#decaseq = [0,0,0,0,0,0,0,0,0,0]

filename = "partition.txt"
f = open(filename, "w")
i = 1

def format2qlist(var, value, numb=0 ):
  qlistline = "0 " + var + str(numb) + " " + str(value) + ";"
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

def whileformat(name,var,size):
  j = 0
  while j < size:
    format2qlist(name, var[j], j)
    j += 1

def whileforformat(name,size):
  j = 0
  while j < size:
    for element in name:
      format2qlist(element[size], element[j], j)
    j += 1

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

#global seqcpt1,seqcpt2 
seqcpt1 = minnt
seqcpt2 = maxpm

#global bpm, seql
bpm = daynumb * 2 + 70
seql = 10

usedeca = 1 #if set to 0 decaseq needs to be mannualy set
usedeca4offset = 1

decaseq = [0,0,0,0,0,0,0,0,0,0]
decaseqoffset = [0,0,0,0,0,0,0,0,0,0]

skeletonset = [4,2,2,10,0,7,2,10]
#skeletonset = [4,2,2,2,0,1,2,10]


osc1s = [1,1500,1000,2, "osc1s"]
osc2s = [2,0,850,1, "osc2s"]
osc3s = [2,102,800,1, "osc3s"]
osc4s = [4,4000,1800,2, "osc4s"]


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
  print("chmod done")


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

if usedeca == 1:
  decaseqmaker(seqcpt1, seqcpt2)

if usedeca4offset == 1:
  decaseqoffset = decaseq

cmxs = [cm1s,cm2s,cm3s,cm4s]
pnpwbs = [pnba,pnbb,pnbc,pnbd,ppba,ppbb,ppbc,ppbd,pwba,pwbb,pwbc,pwbd]
oscss = [osc1s,osc2s,osc3s,osc4s]

whileforformat(cmxs, 4)
whileforformat(pnpwbs,3)
whileforformat(oscss, 4)
format2qlist("bpm", bpm, 1)
format2qlist("seql", seql, 1)
whileformat("dseq",decaseq,10)
whileformat("dseqoff",decaseqoffset,10)
whileformat("sks", skeletonset, 8)
#whileformat("hum", hums[0], 10)
format2qlist("pEDOset",pEDOset)
whileformat("ppqtset",ppqtset,20)


f.close()
