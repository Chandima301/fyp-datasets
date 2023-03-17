from stellargraph import StellarGraph
import pandas as pd
import networkx as nx


def create_node_features(edge_list, node_degree=False, page_rank=False, graph_coloring=False, triangle_count=False):
    print("Creating node features")
    edge_df = pd.DataFrame(edge_list, columns=["source", "target", "timestamp", "weight"])

    graph = StellarGraph(edges=edge_df)
    networkx_graph = graph.to_networkx()

    node_degree_dict = {}
    max_node_degree = 0
    if node_degree:
        print("-Calculating node degrees")
        node_degree_dict = dict(graph.node_degrees())
        max_node_degree = max(node_degree_dict.values())

    pagerank_dict = {}
    if page_rank:
        print("-Calculating page ranks")
        pagerank_dict = nx.pagerank(networkx_graph)

    graph_color_dict = {}
    no_of_colors = 0
    if graph_coloring:
        print("-Coloring nodes")
        graph_color_dict = nx.greedy_color(networkx_graph)
        no_of_colors = max(graph_color_dict.values())

    graph_triangles_dict = {}
    max_triangles = 0
    if triangle_count:
        print("-Calculating triangles")
        graph_triangles_dict = nx.triangles(nx.Graph(networkx_graph))
        max_triangles = max(graph_triangles_dict.values())

    node_features_list = []

    for key in graph.nodes():
        temp = [key]
        if node_degree:
            temp += [node_degree_dict[key]/max_node_degree]
        if page_rank:
            temp += [pagerank_dict[key]]
        if triangle_count:
            temp += [graph_triangles_dict[key]/max_triangles]
        if graph_coloring:
            color_one_hot = [0] * (no_of_colors + 1)
            color_one_hot[graph_color_dict[key]] = 1
            temp += color_one_hot

        node_features_list.append(temp)

    return list(node_features_list)