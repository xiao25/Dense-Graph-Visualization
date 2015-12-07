import json
import re

def map_xy(nodes, svgw, svgh, scale):
    """
    scale x, y in nodes
    find x_min, x_max, y_min, y_max of nodes
    map it to scale of (0,0), (svgw,svgh)
    """
    xs = [float(nd['x']) for nd in nodes]
    ys = [float(nd['y']) for nd in nodes]
    xmin = min(xs); xmax = max(xs); ymin = min(ys); ymax = max(ys)
    for i in xrange(len(nodes)):
        x = float(nodes[i]['x'])
        y = float(nodes[i]['y'])
        if xmax != xmin:
            nodes[i]['x'] = ( svgw / (xmax - xmin) * (x - xmin) ) * scale
        if ymax != ymin:
            nodes[i]['y'] = ( svgh / (ymax - ymin) * (y - ymin) ) * scale
    return nodes



edge_file = open("/home/x/programming/cs519/programming-language-network/data/sample","r")
edges = []
for line in edge_file:
    parts = line.split(",")
    edge = {}
    edge["source"] = unicode( parts[0] , errors='ignore')
    edge["target"] = unicode( parts[1] , errors='ignore')
    edge["value"] = unicode( parts[2].replace("\n","") , errors='ignore')
    edge["name"] = "trade"
    edges.append(edge)
edge_file.close()


node_file = open("/home/x/programming/cs519/programming-language-network/data/county_location.csv","r")
nodes = []
for line in node_file:
        node = {}
        parts = line.split(",")
        node["group"] = "county"
        node["w"] = 10
        node["h"] = 10
        node["id"] = unicode( parts[1] , errors='ignore')
        node["name"] = unicode(parts[3].replace('"', ''), errors='ignore')
        node["POP10"] = unicode( parts[4] , errors='ignore')
        node["ALAND"] = unicode( parts[6] , errors='ignore')
        node["AWATER"] =unicode( parts[7] , errors='ignore')
        node["x"] = unicode( parts[10] , errors='ignore')
        node["y"] = unicode( parts[11] , errors='ignore')
        node["weight"] = "1.0"
        node["fixed"] = True
        nodes.append(node)

node_file.close()
output  = {}
# for now, only nodes with connections will appear
e_nodes = map(lambda x: [x['source'], x['target']], edges)
e_nodes = list(set(reduce(lambda x, y: x + y, e_nodes)))
f_nodes = filter(lambda x: x['id'] in e_nodes, nodes)
# scale x, y
f_nodes = map_xy(f_nodes, 1366, 300, 0.8)
output["nodes"] = f_nodes
output["links"] = edges

# print(output)
fd = open('county.json', 'w')
json_str = json.dumps(output)
fd.write(json_str)
fd.close()
# print(json_str)

# with open('county.json', 'w') as outfile:
#     json.dumps(output, outfile)
