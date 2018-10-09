import requests,json,re,os,sys
from bs4 import BeautifulSoup
import urllib.request
from pycaption import SCCReader
from bs4 import BeautifulSoup
from pathlib import Path

def save(id,name,year,image,duration,genres):
  j={'data':[]}
  j['data'].append({'id':id})
  j['data'].append({'title':name})
  j['data'].append({'year':year})
  j['data'].append({'duration':duration})
  j['data'].append({'genres':genres})
  with open(str(id)+'.json', 'w') as outfile:
      json.dump(j, outfile)
  os.rename(str(id)+'.json', "fox-data/"+str(id)+'.json')
  urllib.request.urlretrieve(image, str(id)+".jpg")
  os.rename(str(id)+".jpg", "fox-data/"+str(id)+".jpg")
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
  #print("Done")

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

def api_call_2(mv_url):
  url="https://api.fox.com/fbc-content/v1_5/screens/movie-detail/"+mv_url
  headers = {'apiKey': 'abdcbed02c124d393b39e818a4312055'}
  r = requests.get(url, headers=headers)
  parsed = json.loads(r.text)
  try:
    uid=parsed['panels']['member'][0]['items']['member'][0]['latestMovieId']
    duration=parsed['panels']['member'][0]['items']['member'][0]['duration']
    return duration,uid
  except:
    return None,None



def api_call_1():

  for n in range(1,2):
    url="https://api.fox.com/fbc-content/v1_5/screenpanels/597a82c06a379500241da0e0/items?itemsPerPage=25&premiumPackage=&page="+str(n)
    headers = {'apiKey': 'abdcbed02c124d393b39e818a4312055'}
    r = requests.get(url, headers=headers)
    parsed = json.loads(r.text)
    for i in parsed['member']:
      id=i['id']
      genres=i['genres']
      images=i['images']
      #imgs=json.loads(images)
      image=images['seriesList']['SD']
      name=i['name']
      year=i['releaseYear']
      mv_url="https://www.fox.com/movies/"+str(id)
      print("Getting: "+name)
      duration,uid=api_call_2(id)
      if uid != None:
        if Path("fox-data/"+str(uid) + ".srt").is_file():
          print("--Existed--")
        else:
          try:
            get_srt(uid)
            save(uid,name,year,image,duration,genres)
          except:
            pass
      else:
        pass
      #break

api_call_1()