import requests,json,re,os,sys
from bs4 import BeautifulSoup
import urllib.request
from pycaption import SCCReader
from bs4 import BeautifulSoup

def make_srt(url):
  #url="https://static-media.fox.com/dcg/cc/2-guns/XMX1593_24029253693.scc"
  r = requests.get(url)
  contents = SCCReader().read(r.text)
  txt=""
  for i in contents.get_captions('en-US'):
    txt+=str(i)+"\n"
  subsFileHandler = open('sample' + ".srt","w",encoding='utf-8')
  subsFileHandler.write(txt)
  subsFileHandler.close()
  print("Done")
  
def get_srt(url):
  #url="https://www.fox.com/watch/51d1be3a17f6ee6e5d11787dbd6d6ac9/"
  r = requests.get(url)
  links = re.findall('"((http|ftp)s?://.*?)"', r.text)
  scc=""
  for i in links:
    if 'scc' in i[0]:
      scc=i[0]
      break
  if scc !="":
    print("Getting Caption")
    make_srt(scc)
  else:
    print("No Caption")
    
def get_details():
  url="https://www.fox.com/movies/the-book-of-life_2014/"
  r = requests.get(url)
  soupObject = BeautifulSoup(r.text,"lxml")
  soup=soupObject.find('script',{'type':"application/ld+json"})
  #print(soup.text)
  datastore = json.loads(soup.text)
  id=datastore['@id']
  name=datastore['name']
  duration=datastore['timeRequired']
  image=datastore['image']
  rele=datastore['releasedEvent']
  release=rele['startDate']
  p1=r.text.find('genres')
  p2=r.text[p1+9:].find(']')
  gen=r.text[p1+9:p1+9+p2].replace('"','').split(',')
  #print(gen)
  watch="https://www.fox.com/watch/"+str(id)
  get_srt(watch)
  #print(release)
  #print(id,name,duration,image)
get_details()