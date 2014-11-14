from bs4 import BeautifulSoup
import requests
import networkx as nx

def wiki_articles_to_gephi(urls):
    g = nx.Graph()
    for url in urls:
        hrefs = get_links_for_url(url)
        g.add_node(url)
        for h in hrefs:
            g.add_node(h)
        for l in hrefs:
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
            hrefs.append(a.attrs['href'])
    return hrefs

urls = ['http://en.wikipedia.org/wiki/New_York-style_pizza', 'http://en.wikipedia.org/wiki/Chicago-style_pizza']
g = wiki_articles_to_gephi(urls)

degree_sequence=sorted(nx.degree(g).values(),reverse=True)

print degree_sequence

# nx.write_gml(g, '/Users/leonsas/Desktop/nyc_chicago_wiki.gml')