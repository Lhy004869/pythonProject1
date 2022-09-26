import matplotlib.pyplot as plt
import networkx as nx
import GraphSta.Graph.stat as st


def plot_ego(graph, node):
    lis=[]
    for i in range(len(node)):
        if(graph.degree[i]<8000):
            lis.append(i)
    g0=graph
    g0.remove_nodes_from(lis)
    pos=nx.drawing.circular_layout(g0)
    nx.draw(g0,with_labels=True,pos=pos)
    plt.show()
    return


def plotdegree_distribution(graph):
    dg=st.cal_degree_distribution(graph)
    d=dict(nx.degree(graph))
    x=list(range(max(d.values())+1))
    plt.plot(x,dg,ls="-")
    plt.show()
    return