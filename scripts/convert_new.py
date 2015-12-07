import json
import re

def map_xy(nodes, svgw, svgh, scale):
    """
    scale x, y in nodes
    find x_min, x_max, y_min, y_max of nodes
    map it to scale of (0,0), (svgw,svgh)
    """

    xmin = nodes[0]['x']
    xmax = nodes[0]['x']
    ymin = nodes[0]['y']
    ymax = nodes[0]['y']

    for nd in nodes:
        x = nd['x']
        y = nd['y']
        if x < xmin :
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    for i in xrange(len(nodes)):
        x = float(nodes[i]['x'])
        y = float(nodes[i]['y'])
        if xmax != xmin:
            nodes[i]['x'] = ( svgw / (xmax - xmin) * (x - xmin) ) * scale - i*0.006 -900
        if ymax != ymin:
            nodes[i]['y'] = ( svgh / (ymax - ymin) * (y - ymin) ) * scale -600
    return nodes





node_file = open("/Users/ztx/Desktop/CS519_Project/county_location.csv","r")
nodes = []
flag = False

count = 0
for line in node_file:
    if count != 0:
        node = {}
        parts = re.split(",|\t",line)
        node["group"] = "county"
        node["w"] = 10
        node["h"] = 10
        node["id"] = int(parts[1])
        node["name"] = unicode(parts[3].replace("\"",""), errors='ignore')
        node["POP10"] = int(parts[4])
        node["ALAND"] = int( parts[6] )
        node["AWATER"] = int(parts[7])
        node["x"] = float(parts[10] )
        node["y"] = float(parts[11] )
        node["weight"] = "1.0"
        node["fixed"] = True
        nodes.append(node)

    count += 1

node_file.close()



edge_file = open("/Users/ztx/Desktop/CS519_Project/part-r-00000","r")
edges = []
count = 0
for line in edge_file:
    if (count %100) == 0:
        parts = line.split(",")
        edge = {}
        edge["source"] = int(parts[0])
        edge["target"] = int(parts[1])
        edge["value"] =  float(parts[2].replace("\n","") )
        edge["name"] = "trade"
        edges.append(edge)
    count += 1

edge_file.close()


print("finish parsing")


output  = {}


f_nodes = map_xy(nodes, 1366, 300, 0.8)
output["nodes"] = f_nodes
output["links"] = edges


fd = open('county_10000.json', 'w')
json_str = json.dumps(output)
fd.write(json_str)
fd.close()

