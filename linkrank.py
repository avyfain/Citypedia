from bs4 import BeautifulSoup
import requests
import threading
import operator

def links_for_city(city):
    url = 'https://en.wikipedia.org/wiki/' + city
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html)
    
    bodyc=soup.find("div", { "id" : "bodyContent" })

    to_remove = ["refbegin", "reflist"]

    for klas in to_remove:
        for tag in bodyc.findAll('div', {"class" : klas}):
            tag.decompose()

    links = bodyc.findAll('a')
    hrefs = []
    for a in links:
        if 'href' in a.attrs and a.attrs['href'].startswith('/wiki/')\
                             and not a.attrs['href'].startswith('/wiki/Category:')\
                             and not a.attrs['href'].startswith('/wiki/Portal:') \
                             and not a.attrs['href'].startswith('/wiki/Help:') \
                             and not a.attrs['href'].startswith('/wiki/File:') \
                             and not a.attrs['href'].startswith('/wiki/Wikipedia:'):
            name = a.attrs['href']
            name = name.replace('/wiki/', '')
            hrefs.append(name)
    
    # # uncomment this to make links unique
    # hrefs = list(set(hrefs))
    return hrefs

def handler(outList,c):
    outList.append(links_for_city(c))

def doStuffWith(city):
    result = []
    thread = threading.Thread(target=handler, args=(result,city))
    return (thread, result)

def main():
    out = []
    cities = ["London","New_York_City","Hong_Kong","Paris","Singapore","Shanghai","Tokyo","Beijing","Sydney","Dubai","Chicago","Mumbai","Milan","Moscow","Sao_Paulo","Frankfurt","Toronto","Los_Angeles","Madrid","Mexico_City","Amsterdam","Kuala_Lumpur","Brussels","Seoul","Johannesburg","Buenos_Aires","Vienna","San_Francisco","Istanbul","Jakarta","Zurich","Warsaw","Washington,_D.C.","Melbourne","New_Delhi","Miami","Barcelona","Bangkok","Boston","Dublin","Taipei","Munich","Stockholm","Prague","Atlanta","Tel_Aviv"]
    threads = [ doStuffWith(c) for c in cities[:10] ]
    for t in threads:
        t[0].start()
    for t in threads:
        t[0].join()
        ret = t[1][0]
        out.append(ret)

    out = [link for city in out for link in city]

    outlinks = {}
    for l in out:
        try:
            outlinks[l] +=1
        except KeyError:
            outlinks[l] = 1

    num_links = float(sum(outlinks.values()))
    for k, v in outlinks.iteritems():
        outlinks[k] = v/num_links

    print outlinks

    # print max(outlinks.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
    main()

