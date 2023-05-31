import requests
from bs4 import BeautifulSoup as bs
from csv import writer
final_links={}
url_q=[]
seed_url="https://www.geeksforgeeks.org/"
url_q.append([seed_url,""])
n=1
visited={}
dataset=[]
nlist=[]
count=1
with open("Crawled_url_final.csv","w",encoding="utf8",newline="") as f:
    write=writer(f)
    header=["url","h1","p","parent"]
    write.writerow(header)
    while(n>0):
        try:
            if("www.geeksforgeeks.org" not in url_q[0][0]):
                url_q.pop(0)
                n-=1
                continue
            if(url_q[0][0]==None):
                url_q.pop(0)
                n-=1
                continue
            print(count,n,url_q[0])
            count+=1
            try:
                web_page=requests.get(url_q[0][0])
            except :
                n-=1
                url_q.pop(0)
                continue
            web_page=bs(web_page.content,"html.parser")
            links=web_page.find_all("a")
            data1=web_page.find_all("h1")
            h1=""
            for i in data1:
                h1+=i.text
            data2=web_page.find_all("p")
            p=""
            for i in data2:
                p+=i.text
            row=[url_q[0][0],h1,p,url_q[0][1]]
            write.writerow(row)
            for link in links:
                curr_url=link.get("href")
                if("www.geeksforgeeks.org" not in curr_url):
                    continue
                try:
                    if(visited[curr_url]!=None):
                        continue
                except KeyError:
                    visited[curr_url]=["-","-"]
                    url_q.append([curr_url,url_q[0][0]])
                    n+=1
            url_q.pop(0)
            n-=1
        except:
            url_q.pop(0)
            n-=1
            continue