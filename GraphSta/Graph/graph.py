import networkx as nx
import  json
from networkx.readwrite import  json_graph
def init_graph(node_list,edge_list):
    G=nx.Graph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    return G




def save_graph(graph):
    out_file= open("D:\pythonProject1\work.json","w")
    json.dump(json_graph.node_link_data(graph),out_file)
    out_file.close()
    return


def load_graph(file):
    with open(file) as fr:
        js_graph=json.load(fr)
        return json_graph.node_link_graph(js_graph)