import orjson
import networkx
import csv
import gc

def create_edges(authors, paper_dict, author_affiliations):
    global author_map
    temp_author_set = set()

    try:
        timestamp = paper_dict["year"]
    except KeyError:
        return [], []

    edges = []

    for author in authors:
        if author["id"] not in author_map:
            author_map[author["id"]] = len(author_map)

    for author in authors:
        author_country = author["org"].split(",")[-1].strip().lower()

        for co_author in authors:
            co_author_country = co_author["org"].split(",")[-1].strip().lower()

            if co_author["id"] != author["id"] and author_country == co_author_country and author_country.lower() in author_affiliations:
                edges += [[author_map[author["id"]], author_map[co_author["id"]], {"timestamp": timestamp}, author_country]]
                temp_author_set.add((author_map[author["id"]], author_country))
                temp_author_set.add((author_map[co_author["id"]], co_author_country))

    return temp_author_set, edges


def get_feature_vector(selected_attr, author, attr):
    global author_data, author_set
    if author not in author_set:
        author_set.add(author)
        feature_attr = [0] * (len(selected_attr))
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
    for i in range(len(selected_attr)):
        try:
            # Update with author fos weight
            feature_attr[i] = max(feature_attr[i], fields[selected_attr[i]])
        except KeyError:
            # Author doesnt have field
            continue

    return feature_attr


def create_attr(authors, paper_dict, selected_attr):
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

    for author_id, author_country in authors:

        attr["n_citation"] = citation_count
        if fos != []:
            attr["fos"] = fos

        author_data[author_id] = get_feature_vector(selected_attr, author_id, attr) + [author_country]


def create_dataset():
    global paper_data
    count = 1

    with open("author_affiliations.txt", "r") as author_affiliations_file:
        reader = csv.reader(author_affiliations_file, delimiter=' ')
        author_affiliations = [str(row[0]).replace('"', '').lower() for row in reader]

    print("No of author affiliations: ", len(author_affiliations))

    with open("co_author_selected_attr.txt", "r") as selected_attr_file:
        reader = csv.reader(selected_attr_file, delimiter=' ')
        selected_attr = [str(row[0]).replace('"', '').lower() for row in reader]

    print("No of author selected attributes: ", len(selected_attr))

    output_edges = []

    with open("../../datasets/dblp_v14.txt", "r") as dblp_file:
        print("File opened")

        for line in dblp_file:

            paper_dict = orjson.loads(line[:-2])
            authors_temp = paper_dict["authors"]

            authors, edges = create_edges(authors_temp, paper_dict, author_affiliations)

            output_edges.extend(edges)

            del authors_temp

            create_attr(authors, paper_dict, selected_attr)

            if count % 100000 == 0:
                # output the current stored paper_id attributes into a json and clear memory
                gc.collect()
                print(count)

            count += 1
            del authors, paper_dict

    sorted_output_edges = sorted(output_edges, key=lambda edge: edge[2]["timestamp"])

    print("Writing edgelist")

    for country in author_affiliations:
        with open("./federated_partitioned/" + country + "_co_author_edgelist.csv", "w+", newline='') as co_author_attr:
            writer = csv.writer(co_author_attr, delimiter=",")
            writer.writerow(["source", "target", "timestamp"])
            for edge in sorted_output_edges:
                if edge[3] == country:
                    writer.writerow([edge[0], edge[1], edge[2]["timestamp"]])

    # output the last stored paper_id attributes into a json and clear memory
    print(count)
    author_items = author_data.items()

    # del paper_data
    print("Writing fos", len(author_data[0]))  # 4107340

    for country in author_affiliations:
        with open(f"./federated_partitioned/" + country + "_co_author_attr.csv", "w+", newline='') as co_author_attr:
            writer = csv.writer(co_author_attr, delimiter=",")
            for id, vector in author_items:
                data = [id] + vector[:-1]
                writer.writerow(data)
    del author_items


if __name__ == "__main__":
    author_data = dict()
    author_set = set([])
    author_map = dict()
    create_dataset()