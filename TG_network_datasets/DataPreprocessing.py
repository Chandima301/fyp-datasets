import csv


def read_dataset():
    print("Preprocessing dataset")
    edge_list = []
    user_id_list = []
    item_id_list = []
    node_list = []
    with open("../../TG_network_datasets/Flights/Flights.csv", "r") as f:
        s = next(f)  # skip the first line
        for idx, line in enumerate(f):
            e = line.strip().split(',')
            u = int(e[0])  # user_id
            i = int(e[1])  # item_id

            if u not in user_id_list:
                user_id_list.append(u)
            if i not in item_id_list:
                item_id_list.append(i)

            ts = float(e[2])  # timestamp  --> assumed in ascending order (I've checked it)

            edge_list.append([u, i, ts])
            node_list.extend(user_id_list)
            node_list.extend(item_id_list)

    return edge_list, node_list


def preprocess_dataset():
    n_node_feat = 8
    edge_list, node_list = read_dataset()
    node_list.sort()

    node_features_list = []

    # add node features
    for node in node_list:
        node_features_list.append([node] + [0] * n_node_feat)

    save_dataset(edge_list, node_features_list)


def save_dataset(edge_list, node_features_list):
    print("Writing edgelist", len(edge_list))
    with open("edgelist_with_timestamp.csv", "w+", newline='') as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
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
