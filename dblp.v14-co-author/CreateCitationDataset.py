import orjson
import json
import networkx
import csv
import gc


# 36545646
# 36624464 new
def create_edges(author_ids, paper_dict):
    global author_map
    temp_author_set = set()

    try:
        timestamp = paper_dict["year"]
    except KeyError:
        return [], []

    for id in author_ids:
        if id not in author_map:
            author_map[id] = len(author_map)

        temp_author_set.add(author_map[id])

    edges = []

    for author_id in temp_author_set:
        author_relations = temp_author_set - {author_id}

        edges += [(author_id, co_author, {"timestamp": timestamp}) for co_author in author_relations]

    return temp_author_set, edges


def get_feature_vector(selected_attr, author, attr, N):
    global author_data, author_set
    if author not in author_set:
        author_set.add(author)
        feature_attr = [0] * (N)
        # feature_attr[0] = attr["n_citation"]
    else:
        feature_attr = author_data[author]
        # feature_attr[0] += attr["n_citation"]

    try:
        fields = {item[0].lower(): item[1] for item in attr["fos"]}
    except KeyError:
        # fos key missing in data
        return feature_attr

    # Increment the no of appearencs count / no of authors in the partial file
    for i in range(N):
        try:
            # Update with author fos weight
            feature_attr[i] = max(feature_attr[i], fields[selected_attr[i]])
        except KeyError:
            # Author doesnt have field
            continue

    return feature_attr


def create_attr(authors, paper_dict, selected_attr, N):
    global author_data
    try:
        fos = [list(item.values()) for item in paper_dict["fos"]]
    except KeyError:
        # Fos key missing in data
        fos = []

    try:
        citation_count = paper_dict["n_citation"]
    except KeyError:
        # n_citation key missing in data
        citation_count = 0

    attr = dict()

    for author_id in authors:

        attr["n_citation"] = citation_count
        if fos != []:
            attr["fos"] = fos

        author_data[author_id] = get_feature_vector(selected_attr, author_id, attr, N)


def create_dataset():
    """
    Generates generates partial json files of the following formatnano
    {
        "<paper_id pid>" : {
            "<name>" : "<>"
            "<no of citations>" : <>
            "<fields of study>" : [["<>", <>],...]
        },...
    }
    :return:
    """
    global paper_data
    count = 1
    fos_missing_count = 0
    # full_data = dict()

    with open("co_author_selected_attr.txt", "r") as selected_attr_file:
        reader = csv.reader(selected_attr_file, delimiter=' ')
        selected_attr = [str(row[0]).replace('"', '').lower() for row in reader]

    N = len(selected_attr)
    print(N)

    G = networkx.DiGraph()

    with open("../../datasets/dblp_v14.txt", "r") as dblp_file:
        print("File opened")

        for line in dblp_file:

            paper_dict = orjson.loads(line[:-2])
            authors_temp = set([tuple(item.values()) for item in paper_dict["authors"]])
            author_ids = set([list(author)[1] for author in authors_temp])

            authors, edges = create_edges(author_ids, paper_dict)

            G.add_nodes_from(authors)
            G.add_edges_from(edges)

            del authors_temp, author_ids

            create_attr(authors, paper_dict, selected_attr, N)

            if count % 100000 == 0:
                # output the current stored paper_id attributes into a json and clear memory
                gc.collect()
                print(count)

            count += 1
            del authors, paper_dict

    E = G.edges.data()
    print("Writing edgelist", len(E))
    with open("co_author_edgelist.csv", "w+", newline='') as co_author_attr:
        writer = csv.writer(co_author_attr, delimiter=",")
        for edge in E:
            writer.writerow([edge[0], edge[1], edge[2]["timestamp"]])

    # output the last stored paper_id attributes into a json and clear memory
    print(count)
    paper_items = paper_data.items()

    # del paper_data
    print("Writing fos", len(paper_data[0]))  # 4107340
    with open(f"co_author_attr.csv", "w+", newline='') as co_author_attr:
        writer = csv.writer(co_author_attr, delimiter=",")
        for id, vector in paper_items:
            data = [id] + vector
            writer.writerow(data)
    del paper_items


if __name__ == "__main__":
    author_data = dict()
    author_set = set([])
    author_map = dict()
    create_dataset()  # 3655052 11697041