from utils.create_node_features import create_node_features
from utils.save_dataset import save_dataset


def read_dataset(file_path):
    print("Reading dataset")
    edge_list = []
    with open(file_path, "r") as f:
        s = next(f)  # skip the first line
        for idx, line in enumerate(f):
            e = line.strip().split(',')
            u = int(e[0])  # user_id
            i = int(e[1])  # item_id

            edge_features = [1]
            ts = float(e[2])  # timestamp  --> assumed in ascending order
            edge_list.append([u, i, ts] + edge_features)

    return edge_list


if __name__ == "__main__":
    edges = read_dataset("../../TG_network_datasets/wikipedia/wikipedia.csv")
    node_features = create_node_features(edges, node_degree=True, page_rank=False, graph_coloring=True,
                                         triangle_count=True)
    save_dataset(edges, node_features, edge_list_file_path="wikipedia_edges.csv",
                 node_list_file_path="wikipedia_nodes.csv")
