from utils.create_node_features import create_node_features
from utils.save_dataset import save_dataset


def read_dataset(file_path):
    print("Reading dataset")
    edge_list = []
    count = 1
    with open(file_path, "r") as f:
        # s = next(f)  # skip the first line
        for idx, line in enumerate(f):
            e = line.strip().split(',')
            u = int(e[0])  # source id
            i = int(e[1])  # target id

            rating = float(e[2])
            ts = float(count)  # timestamp  --> assumed in ascending order (I've checked it)
            edge_list.append([u, i, ts, rating])
            count += 1

    return edge_list


if __name__ == "__main__":
    edges = read_dataset("../../datasets/soc-sign-bitcoinotc.csv")
    node_features = create_node_features(edges, node_degree=True, page_rank=False, graph_coloring=True, triangle_count=True)
    save_dataset(edges, node_features, edge_list_file_path="bitcoin_edges.csv", node_list_file_path="bitcoin_nodes.csv")
