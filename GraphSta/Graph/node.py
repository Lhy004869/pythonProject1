import csv


def init_node(file_node):
    node_dic={}
    with open(file_node, 'r', encoding='utf-8') as csv_file:
        file=csv.reader(csv_file)
        a=0
        for i in file:
            if a>0:
                dic = {}
                dic["views"] = int(i[0])
                dic["mature"] = int(i[1])
                dic["lifetime"] = int(i[2])
                dic["created_at"] = i[3]
                dic["updated_at"] = i[4]
                dic["dead_account"] = int(i[6])
                dic["language"] = i[7]
                dic["affiliate"] = int(i[8])
                node_dic[int(i[5])] = dic
            a+=1
    return node_dic


def init_edge(file_path):
    edge_list=[]
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        file=csv.reader(csv_file)
        a=0
        for item in file:
            if a>0:
                ed=tuple([int(item[0]),int(item[1])])
                edge_list.append(ed)
            a+=1
    return edge_list


def get_views(node):
    return node["views"]


def get_degree(index,G):
    return G.degree[index]


def print_node(node):
    print("views:{0[views]};mature:{0[mature]};lifetime:{0[lifetime]};created_at:{0[created_at]};updated_at:{0[updated_at]};dead_account:{0[dead_account]};language:{0[language]};affiliate:{0[affiliate]}".format(node))
    return
