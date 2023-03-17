import csv


def save_dataset(edge_list, node_features_list, edge_list_file_path, node_list_file_path):
    print("Saving dataset")
    print("-Writing edgelist", len(edge_list))
    with open(edge_list_file_path, "w+", newline='') as edge_file:
        writer = csv.writer(edge_file, delimiter=",")
        first_line = ["source", "target", "timestamp", "weight"]
        writer.writerow(first_line)
        for edge in edge_list:
            writer.writerow(edge)

    print("-Writing node features", len(node_features_list))
    with open(node_list_file_path, "w+", newline='') as node_file:
        writer = csv.writer(node_file, delimiter=",")
        first_line = ["node"]
        for k in range(len(node_features_list[1]) - 1):
            first_line.append("feature_" + str(k + 1))
        writer.writerow(first_line)
        for node in node_features_list:
            writer.writerow(node)