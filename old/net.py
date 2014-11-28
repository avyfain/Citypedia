from bs4 import BeautifulSoup
import requests
import networkx as nx

def wiki_articles_to_gephi(urls, g, maxlevel):
    for url in urls:
        if url[1] < maxlevel:
            hrefs = get_links_for_url(url[0])
            g.add_node(url[0])
            print url[0]
            for h in hrefs:
                if not g.has_node(h):
                    g.add_node(h)
                    urls.append(('https://en.wikipedia.org/wiki/'+h,url[1]+1))
            for l in hrefs:
                if not g.has_edge(url, l):
                    g.add_edge(url, l)
    print "returning"
    return g

                
def get_links_for_url(url):
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html)
    soup.find("div", { "id" : "bodyContent" })
    bodyc=soup.find("div", { "id" : "bodyContent" })
    links = bodyc.findAll('a')
    hrefs = []
    for a in links:
        if 'href' in a.attrs and a.attrs['href'].startswith('/wiki/'):
            name = a.attrs['href']
            name = name.replace('/wiki/', '')
            hrefs.append(name)
    return hrefs

urls = [('https://en.wikipedia.org/wiki/New_York_City',0), ('https://en.wikipedia.org/wiki/Chicago',0)]
g = nx.Graph()
g = wiki_articles_to_gephi(urls, g, 2)
nx.write_gml(g, 'nyc_chicago_wiki.gml')