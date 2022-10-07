import matplotlib.pyplot as plt

import  GraphSta.Graph.stat as st


def plot_nodes_attr(graph,attr):
    fq = []
    num = st.get_node_number(graph)
    for i in range(num):
        fq.append(graph.nodes[i][attr])
    dis = [0 for k in range((max(fq) + 1))]
    for i in range(num):
        att = graph.nodes[i][attr]
        dis[att] += 1
    x = list(range(max(fq) + 1))
    plt.plot(x,dis,"-")
    plt.show()
    return