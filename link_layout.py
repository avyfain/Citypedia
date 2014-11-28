import operator
import urllib
import json
from jinja2 import Template
bin_breaks = {'Chicago':        [0.004015172595221041, 0.0020075862976105204, 0.0014292407151658435, 0.0008027006705568285,-1],\
              'London':         [0.003379342946188495, 0.0016896714730942476, 0.001006416505027073, 0.0005324253825028401,-1],\
              'New_York_City':  [0.005967983904967859, 0.0019893279683226195, 0.0014162422464871957, 0.0009620825570832646,-1],\
              'Paris':          [0.003920313120466328, 0.001960156560233164, 0.0016778155498217812, 0.0007010761311666402,-1],\
              'Tokyo':          [0.009380476326262021, 0.0031268254420873404, 0.0015687388450773532, 0.0010894672770911421,-1]}

colors = ['#243392', '#2962ff', '#3d9dfd', '#8fc6ff', '#e2f0ff'];

template_str = """
<!DOCTYPE html>
<html>
<style>
.container {
    height:{{height}};
    width:9000px;
}

.terms {
    width: 50%;
    margin: 0 auto;
    position: relative;
    top: 50%;
    transform: translateY(-50%);
}

p { 
    font-family: sans-serif; 
    text-align: center; 
    display:inline-block; 
    margin-top:7px;margin-bottom:7px; 
    font-size:80px
}

a {
    color: white; 
    padding: 2px;
}
</style>
<body style="text-align: justify;">
    <div class="container">
        <div class="terms">
            {% for link in links %}
                <p class="term"><a style="background: {{link[0]}};">{{link[1]}}</a></p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

with open("link_data.json") as json_file:
    linkranks = json.load(json_file)
    lengths = {'Chicago':'41502',
              'London':'41070',
              'New_York_City':'47284',
              'Paris':'48743',
              'Tokyo':'32551'}

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
        html = t.render(links=links_w_colors, height=lenghts[city])
        html = html.encode('utf-8')
        f = open(city + '.html','w')
        f.write(html)