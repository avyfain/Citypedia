from links import linkranks
import requests
import threading
from collections import Counter, defaultdict
import math
import json
import operator
import urllib
from jinja2 import Template
bin_breaks = {'Chicago':        [0.004015172595221041, 0.0020075862976105204, 0.0014292407151658435, 0.0008027006705568285,-1],\
              'London':         [0.003379342946188495, 0.0016896714730942476, 0.001006416505027073, 0.0005324253825028401,-1],\
              'New_York_City':  [0.005967983904967859, 0.0019893279683226195, 0.0014162422464871957, 0.0009620825570832646,-1],\
              'Paris':          [0.003920313120466328, 0.001960156560233164, 0.0016778155498217812, 0.0007010761311666402,-1],\
              'Tokyo':          [0.009380476326262021, 0.0031268254420873404, 0.0015687388450773532, 0.0010894672770911421,-1]};

colors = ['#243392', '#2962ff', '#3d9dfd', '#8fc6ff', '#e2f0ff'];

# html_top = \
# '''
# <!DOCTYPE html>
# <html>
# <body>
# '''

# html_bottom = \
# '''
# </body>
# </html>
# '''

# for city, links in linkranks.items():
#   Html_file= open(city + ".html","w")
#   Html_file.write(html_top)
#   sorted_links = sorted(links.items(), key=operator.itemgetter(1), reverse=True)
#   color_val = 0
#   for link in sorted_links:
#     if link[1] < bin_breaks[city][color_val]:
#       color_val+=1
#     the_vars = (colors[color_val], urllib.unquote(link[0]).replace('_', ' '))
#     html_str = '''<p style="text-align: center;"><a style="background: %s; color: white; padding: 2px;">%s</a></p>\n''' % the_vars
#     html_str = html_str.encode('utf-8')
#     Html_file.write(html_str)
#   Html_file.write(html_bottom)
#   Html_file.close()

# for city, links in linkranks.items():
#   Html_file= open(city + ".html","w")
#   Html_file.write(html_top)
#   sorted_links = sorted(links.items(), key=operator.itemgetter(1), reverse=True)
#   color_val = 0
#   for link in sorted_links:
#     if link[1] < bin_breaks[city][color_val]:
#       color_val+=1
#     the_vars = (colors[color_val], urllib.unquote(link[0]).replace('_', ' '))
#     html_str = '''<p style="text-align: center;"><a style="background: %s; color: white; padding: 2px;">%s</a></p>\n''' % the_vars
#     html_str = html_str.encode('utf-8')
#     Html_file.write(html_str)
#   Html_file.write(html_bottom)
#   Html_file.close()

template_str = """
<!DOCTYPE html>
<html>
<body style="text-align: justify;">
{% for link in links %}
    <p style="text-align: center; display:inline-block; margin-top:7px;margin-bottom:7px; font-size:32px;" class="term"><a style="background: {{link[0]}}; color: white; padding: 2px;">{{link[1]}}</a></p>
{% endfor %}
</body>
</html>
"""

for city, links in linkranks.items():
    formatted_link = []
    sorted_links = sorted(links.items(), key=operator.itemgetter(1), reverse=True)
    links_w_colors = []
    color_val=0
    for link in sorted_links:
        if link[1] < bin_breaks[city][color_val]:
            color_val+=1
        unquoted = urllib.unquote_plus(link[0])
        unquoted = unquoted.replace('_', ' ')
        links_w_colors.append((colors[color_val], unquoted.decode('utf-8')))

    t = Template(template_str)
    html = t.render(links=links_w_colors)
    html = html.encode('utf-8')
    f = open(city + '.html','w')
    f.write(html)