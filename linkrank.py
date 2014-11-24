from bs4 import BeautifulSoup
import requests
import threading
from collections import Counter, defaultdict
import math
import json
import operator
import urllib

def get_idfs(dicts):
    idfs = defaultdict(float)
    for city_dict in dicts.values():
        for link in city_dict.keys():
            idfs[link] += 1

    num_docs = float(len(dicts.keys()))
    for link, term_count in idfs.items():
        idfs[link] = math.log(num_docs/term_count)
    return dict(idfs)

def get_tf(city_dict):
    total = sum(city_dict.values(), 0.0)
    for key in city_dict:
        city_dict[key] /= total
    return city_dict

def links_for_city(city):
    url = 'https://en.wikipedia.org/wiki/' + city
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html)
    bodyc = soup.find("div", { "id" : "bodyContent" })
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
                             and not a.attrs['href'].startswith('/wiki/Wikipedia:')\
                             and not a.attrs['href'].startswith('/wiki/Special:')\
                             and not a.attrs['href'].startswith('/wiki/Template:')\
                             and not a.attrs['href'].startswith('/wiki/Template_talk:')\
                             and not a.attrs['href'].startswith('/wiki/International_Standard_Book_Number'):
            name = a.attrs['href']
            name = name.replace('/wiki/', '')
            hrefs.append(name)
    counts = Counter(hrefs)
    normalized_counts = get_tf(counts)
    return normalized_counts

def handler(result,c):
    result.append(links_for_city(c))
    return result

def doStuffWith(city):
    result = []
    thread = threading.Thread(target=handler, args=(result,city))
    return (thread, city, result)

def main():
    cities_dict = {}
    cities = ["London","New_York_City","Hong_Kong","Paris","Singapore","Shanghai",\
              "Tokyo","Beijing","Sydney","Dubai","Chicago","Mumbai","Milan","Moscow","Sao_Paulo",\
              "Frankfurt","Toronto","Los_Angeles","Madrid","Mexico_City","Amsterdam","Kuala_Lumpur",\
              "Brussels","Seoul","Johannesburg","Buenos_Aires","Vienna","San_Francisco","Istanbul",\
              "Jakarta","Zurich","Warsaw","Washington,_D.C.","Melbourne","New_Delhi","Miami",\
              "Barcelona","Bangkok","Boston","Dublin","Taipei","Munich","Stockholm","Prague",\
              "Atlanta","Bangalore","Lisbon","Copenhagen","Santiago","Guangzhou","Rome","Cairo",\
              "Dallas","Hamburg","Dusseldorf","Athens","Manila","Montreal","Philadelphia","Tel_Aviv",\
              "Lima","Budapest","Berlin","Cape_Town","Luxembourg_(city)","Houston","Kiev","Bucharest",\
              "Beirut","Ho_Chi_Minh_City","Bogota","Auckland","Montevideo","Caracas","Riyadh",\
              "Vancouver","Chennai","Manchester","Oslo","Brisbane","Helsinki","Karachi","Doha",\
              "Casablanca","Stuttgart","Rio_de_Janeiro","Geneva","Guatemala_City","Lyon","Monterrey",\
              "Panama_City","San_Jose,_Costa_Rica","Bratislava","Minneapolis","Tunis","Nairobi",\
              "Cleveland","Lagos","Abu_Dhabi","Seattle","Hanoi","Sofia","Riga","Port_Louis","Detroit",\
              "Calgary","Denver","Perth","Kolkata","San_Diego","Amman","Antwerp","Manama","Birmingham",\
              "Nicosia","Quito","Rotterdam","Belgrade","Almaty","Shenzhen","Kuwait_City",\
              "Hyderabad,_India","Edinburgh"]
    threads = [ doStuffWith(c) for c in cities]
    for t in threads:
        t[0].start()
    for t in threads:
        t[0].join()
        cities_dict[t[1]] = t[2][0]

    corpus = get_idfs(cities_dict)

    our_cities = ["London","New_York_City", "Chicago", "Paris", "Tokyo"]
    out_dict = {}
    for c in our_cities:
        out_dict[c] = cities_dict[c]
        for k,v in out_dict[c].items():
            out_dict[c][k] = out_dict[c][k]*corpus[k]

    print json.dumps(out_dict, ensure_ascii=False)

    bin_breaks = {'Chicago':        [0.004015172595221041, 0.0020075862976105204, 0.0014292407151658435, 0.0008027006705568285,-1],\
                  'London':         [0.003379342946188495, 0.0016896714730942476, 0.001006416505027073, 0.0005324253825028401,-1],\
                  'New_York_City':  [0.005967983904967859, 0.0019893279683226195, 0.0014162422464871957, 0.0009620825570832646,-1],\
                  'Paris':          [0.003920313120466328, 0.001960156560233164, 0.0016778155498217812, 0.0007010761311666402,-1],\
                  'Tokyo':          [0.009380476326262021, 0.0031268254420873404, 0.0015687388450773532, 0.0010894672770911421,-1]};

    colors = ['#243392', '#2962ff', '#3d9dfd', '#8fc6ff', '#e2f0ff'];

    html_top = \
    '''
    <!DOCTYPE html>
    <html>
    <body>
    '''

    html_bottom = \
    '''
    </body>
    </html>
    '''

    for city, links in out_dict.items():
      Html_file= open(city + ".html","w")
      Html_file.write(html_top)
      sorted_links = sorted(links.items(), key=operator.itemgetter(1), reverse=True)
      color_val = 0
      for link in sorted_links:
        if link[1] < bin_breaks[city][color_val]:
          color_val+=1
        the_vars = (colors[color_val], urllib.unquote(link[0]).replace('_', ' '))
        html_str = '''<p style="text-align: center;"><a style="background: %s; color: white; padding: 2px;">%s</a></p>\n''' % the_vars
        Html_file.write(html_str)
      Html_file.write(html_bottom)
      Html_file.close()

if __name__ == '__main__':
    main()