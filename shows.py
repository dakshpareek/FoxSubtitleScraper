import requests,json,re,os,sys
from bs4 import BeautifulSoup
import urllib.request
from pycaption import SCCReader
from bs4 import BeautifulSoup

def save(id,name,series,date,image,duration,genres):
  j={'data':[]}
  j['data'].append({'id':id})
  j['data'].append({'title':name})
  j['data'].append({'series':series})
  j['data'].append({'date':date})
  j['data'].append({'duration':duration})
  j['data'].append({'genres':genres})
  with open(str(id)+'.json', 'w') as outfile:
      json.dump(j, outfile)
  os.rename(str(id)+'.json', "fox-data/"+str(id)+'.json')
  urllib.request.urlretrieve(image, str(id)+".jpg")
  os.rename(str(id)+".jpg", "fox-data/"+str(id)+".jpg")
  #print(j)
  print("**---Done---**")

def make_srt(url,uid):
  r = requests.get(url)
  contents = SCCReader().read(r.text)
  txt=""
  for i in contents.get_captions('en-US'):
    txt+=str(i)+"\n"
  subsFileHandler = open(str(uid) + ".srt","w",encoding='utf-8')
  subsFileHandler.write(txt)
  subsFileHandler.close()
  os.rename(str(uid) + ".srt", "fox-data/"+str(uid) + ".srt")
  print("Done")

def get_srt(uid):
  url="https://www.fox.com/watch/"+str(uid)
  r = requests.get(url)
  links = re.findall('"((http|ftp)s?://.*?)"', r.text)
  scc=""
  for i in links:
    if 'scc' in i[0]:
      scc=i[0]
      break
  if scc !="":
    print("Getting Caption")
    make_srt(scc,uid)
  else:
    print("No Caption")


def api2(idd,t_season,image,genres):
  headers = {'apiKey': 'abdcbed02c124d393b39e818a4312055'}
  for k in range(1,t_season+1):
    k=str(k).zfill(2)
    print("Season:"+k)
    url="https://api.fox.com/fbc-content/v1_5/seasons/"+idd+"_"+k+"/episodes/"
    #print(url)
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)
    try:
      videos=parsed['member']
      for i in videos:
        series=i['seriesName']
        date=i['originalAirDate']
        name=i['name']
        id=i['id']
        duration=i['durationInSeconds']/60
        print(name)
        #return duration,id
        get_srt(id)
        save(id,name,series,date,image,duration,genres)
    except:
      pass

def api1():
  for z in range(1,3):
    url1="https://api.fox.com/fbc-content/v1_5/screenpanels/58de915ceffde70001a6e761/items?itemsPerPage=25&premiumPackage=&page="+str(z)
    url="https://api.fox.com/fbc-content/v1_5/screenpanels/58daf2a54672070001df1404/items?itemsPerPage=25&premiumPackage=&page="+str(z)
    headers = {'apiKey': 'abdcbed02c124d393b39e818a4312055'}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)
    #print(parsed)
    for i in parsed['member']:
      t_season=i['seasonCount']
      id=i['id']
      try:
        genres=i['genres']
      except:
        genres=""
      images=i['images']
      image=images['seriesList']['SD']
      name=i['name']
      #mv_url="https://www.fox.com/"+str(id)
      print(name)
      try:
        duration,uid=api2(id,t_season,image,genres)
      except:
        pass
      print("----")
      #break

api1()