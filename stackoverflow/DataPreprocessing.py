from utils.create_node_features import create_node_features_1
from utils.save_dataset import save_dataset
import pandas as pd

def read_dataset(file_path):

    print("preparing edges")
    print("-Reading dataset from csv")
    edge_df = pd.read_csv(file_path, header=None, delim_whitespace=True)
    print("-Done reading dataset from csv !!")
    edge_df.columns = ['source', 'target', 'timestamp']
    print("-Adding timestamp")
    edge_df['timestamp'] = [i for i in range(0, len(edge_df))]
    print(edge_df.head())
    edge_df['weight'] = 1

    print(edge_df.head())

    # edge_dict = {
    #     "source": [],
    #     "target": [],
    #     "timestamp": [],
    #     "weight": []
    # }
    #
    # edge_df = pd.DataFrame(edge_dict)
    #
    # with open(file_path, "r") as f:
    #     s = next(f)  # skip the first line
    #     count = 0
    #     for idx, line in enumerate(f):
    #         e = line.strip().split(' ')
    #         u = int(e[0])  # user_id
    #         i = int(e[1])  # item_id
    #         if count % 100000 == 0:
    #             print(count)
    #         count += 1
    #         ts = float(count)  # timestamp  --> assumed in ascending order
    #         edge_df.append({"source": u, "target": i, "timestamp": ts, "weight": 1}, ignore_index=True)

    return edge_df


if __name__ == "__main__":
    edges = read_dataset("../../datasets/sx-stackoverflow.txt")
    node_features = create_node_features_1(edges, node_degree=True, page_rank=False, graph_coloring=True, triangle_count=True)
    save_dataset(edges, node_features,  edge_list_file_path="stackoverflow_edges.csv", node_list_file_path="stackoverflow_nodes.csv")
