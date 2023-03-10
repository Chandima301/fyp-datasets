import scipy.io as sio
import csv
from collections import Counter

print("Reading trust relations....")
mat_contents = sio.loadmat("epinion_trust_with_timestamp.mat")
print("Structure of trust relations")
print(mat_contents.keys())
print("")
print("Trust relations content")
truststruct = mat_contents['trust']
sorted_trust_relations = sorted(truststruct, key=lambda relation: relation[2])
print(truststruct)

print("Writing edgelist", len(truststruct))
with open("epinion_trust_with_timestamp.csv", "w+", newline='') as edge_file:
    writer = csv.writer(edge_file, delimiter=",")
    writer.writerow(["source", "target", "timestamp"])
    for edge in sorted_trust_relations:
        writer.writerow(edge)

print("")

print("Reading ratings....")
mat_contents = sio.loadmat("rating_with_timestamp.mat")
print("Structure of rating")
print(mat_contents.keys())
print("")
print("Rating content")
ratingstruct = mat_contents['rating']
print(ratingstruct)

user_rating = {}
user_rating_helpfulness = {}
user_categories = {}
all_categories = set()

for node in ratingstruct:
    all_categories.add(node[2])
    try:
        user_rating[node[0]].append(node[3])
        user_rating_helpfulness[node[0]].append(node[4])
        user_categories[node[0]].append(node[2])
    except KeyError:
        user_rating[node[0]] = [node[3]]
        user_rating_helpfulness[node[0]] = [node[4]]
        user_categories[node[0]] = [node[2]]

print("Writing node features", len(ratingstruct))

with open("rating.csv", "w+", newline='') as node_file:
    writer = csv.writer(node_file, delimiter=",")
    first_line = ["node"]
    for a in range(10+len(all_categories)):
        first_line.append("column_"+str(a+1))
    writer.writerow(first_line)

    for user_id in user_rating.keys():

        feature_vector = []

        rating_counts = Counter(user_rating[user_id])
        helpfulness_counts = Counter(user_rating_helpfulness[user_id])
        category_counts = Counter(user_categories[user_id])

        # 5 values for rating
        for i in range(1, 6):
            feature_vector.append(round((rating_counts[i] / len(user_rating[user_id])), 3))

        # 5 values for helpfulness
        for j in range(1, 6):
            feature_vector.append(round((helpfulness_counts[j] / len(user_rating_helpfulness[user_id])), 3))

        product_category_feature_vector = []
        # for product categories
        for k in all_categories:
            product_category_feature_vector.append(round((category_counts[k]/len(user_categories[user_id])), 3))

        writer.writerow([user_id] + feature_vector + product_category_feature_vector)
