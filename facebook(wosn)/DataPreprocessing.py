from utils.create_node_features import create_node_features
from utils.save_dataset import save_dataset


def read_dataset(file_path):
    print("Reading dataset")
    edge_list = []
    count = 1
    with open(file_path, "r") as f:
        line1 = next(f)  # skip the first line
        line2 = next(f)  # skip the second line
        for idx, line in enumerate(f):
            e = line.strip().split(' ')
            u = int(e[0])  # source id
            i = int(e[1])  # target id

            weight = int(e[2])
            ts = int(e[3])
            edge_list.append([u, i, ts, weight])
            count += 1
    edge_list_sorted = sorted(edge_list, key=lambda edge: edge[2])
    return edge_list_sorted


if __name__ == "__main__":
    edges = read_dataset("../../datasets/out.facebook-wosn-links")
    node_features = create_node_features(edges, node_degree=True, page_rank=False, graph_coloring=True, triangle_count=True)
    save_dataset(edges, node_features, edge_list_file_path="facebook_edges.csv", node_list_file_path="facebook_nodes.csv")
