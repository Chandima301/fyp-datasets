import csv


def read_dataset():
    print("Preprocessing dataset")
    edge_list = []
    node_id_list = set()
    with open("../../TG_network_datasets/Flights/Flights.csv", "r") as f:
        s = next(f)  # skip the first line
        for idx, line in enumerate(f):
            e = line.strip().split(',')
            u = int(e[0])  # user_id
            i = int(e[1])  # item_id

            edge_features = [float(i) for i in e[4:]]

            node_id_list.add(u)
            node_id_list.add(i)

            ts = float(e[2])  # timestamp  --> assumed in ascending order (I've checked it)
            edge_list.append([u, i, ts] + edge_features)

    return edge_list, node_id_list


def preprocess_dataset():
    n_node_feat = 8
    edge_list, node_id_list = read_dataset()

    node_features_list = []

    print("Adding node features")
    # add node features
    for node in node_id_list:
        node_features_list.append([node] + [0] * n_node_feat)

    save_dataset(edge_list, node_features_list)


def save_dataset(edge_list, node_features_list):
    print("Writing edgelist", len(edge_list))
    with open("edgelist_with_timestamp.csv", "w+", newline='') as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
        first_line = ["source", "target", "timestamp"]
        for k in range(len(edge_list)-3):
            first_line.append("feature_" + str(k+1))
        writer.writerow(first_line)
        for edge in edge_list:
            writer.writerow(edge)

    print("Writing node features", len(node_features_list))
    with open("node_features.csv", "w+", newline='') as node_file:
        writer = csv.writer(node_file, delimiter=",")
        for node in node_features_list:
            writer.writerow(node)


if __name__ == "__main__":
    paper_data = dict()
    paper_map = dict()
    preprocess_dataset()
