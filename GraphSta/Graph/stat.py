import networkx as nx


def get_node_number(graph):
    return graph.number_of_nodes()


def get_edge_number(graph):
    return graph.number_of_edges()


def cal_average_degree(graph):
    num=get_node_number(graph)
    sum1=0
    for i in range(num):
        sum1+=graph.degree[i]
    ave=sum1/num
    return ave


def cal_degree_distribution(graph):
    return nx.degree_histogram(graph)


def cal_views_distribution(graph):
    vw_fq=[]
    num = get_node_number(graph)
    for i in range(num):
        vw_fq.append(graph.nodes[i]["views"])
    vw_dis=[0 for k in range((max(vw_fq)+1))]
    for i in range(num):
        view=graph.nodes[i]["views"]
        vw_dis[view]+=1
    return  vw_dis