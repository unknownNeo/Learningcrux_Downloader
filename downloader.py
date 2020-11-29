import requests
import io
import sys
import wget
import urllib.parse
from os import path, system
from glob import glob

def decode(url):
    u = urllib.parse.unquote(url)
    return u

get_url = sys.argv[1]
course = get_url.split("/")[4]
domain = "https://www.learningcrux.com/play/"
archive = "https://archive.org/download/"
local = course + ".txt"

def quality_check(domain,course):
    q = ["144","360","480","720","1080"]
    a = []
    print("checking qualities....")
    for i in range(0,len(q)):
        url = domain + course + "/0/0/" + q[i] + "?type=sort"
        #print(url)
        r = requests.get(url,allow_redirects=False)
        if "302" not in str(r):
            continue
        else:
            #print(r.headers['Location'])
            #l = r.headers['Location'].split("/")[4]
            a.append(q[i])
    return a

def download(url):
    r = requests.get(url,allow_redirects=False)
    u = decode(r.headers['Location'])
    url = u.replace(".mp4 ",".mp4")
    wget.download(url)
    print("\n")

def get_links(domain,course,a):
    for i in range(0,len(a)):
        print(str(i+1) + " : " + a[i])

    c = str(input("Which quality you want to download (quality number): "))
    quality = a[int(c) - 1]
    print("you select : " + quality)
    url = domain + course + "/0/0/" + quality + "?type=sort"
    r = requests.get(url,allow_redirects=False)
    l = r.headers['Location'].split("/")[4]
    url = archive + l
    print(url)
    r = requests.get(url)
    f = open(local,"w")
    f.write(r.text)
    f.close()

    print("getting links....")
    f = open(local,"r").readlines()
    w = open(local,"w")
    w.write(url.split("/")[4])
    w.write("\n")
    for line in f:
        if "<td><a " in line:
            if ".mp4" in line:
                w.write(line.split("href=")[1].replace("\">"," : ").replace("</a></td>","").replace("\"",""))
    w.close()
    print("done.....")

def downloaded(file_name):
    files = glob('*.mp4')
    file = file_name.replace(".mp4 ",".mp4")
    if file in files:
        print(file + " : [done]")
        return 1
    else:
        return 0
        
def file_list(local,archive):
    file = open(local,"r").readlines()
    l = file[0]
    for i in range(8,len(file)):
        link = file[i].split(":")[0]
        update = decode(link)
        exists = downloaded(update)
        if exists == 0:
            url = archive + l.replace("\n","") + "/" + update
            print('downloading : ' + update)
            download(url)

    print("All Files Are Downloaded")

ls = glob("./*.txt")
exists = 0
#print(ls)
for i in range(0,len(ls)):
    if local in ls[i]:
        exists = 1
        break
    else:
        exists = 0

if exists == 0:
    print("New Course.....")
    a = quality_check(domain,course)
    #print(a)
    url = get_links(domain,course,a)
    file_list(local,archive)
else:
    print("course link found......")
    print("Getting link......")
    file_list(local,archive)


