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
for node in ratingstruct:
    try:
        user_rating[node[0]].append(node[3])
    except KeyError:
        user_rating[node[0]] = [node[3]]

user_rating_helpfulness = {}
for node in ratingstruct:
    try:
        user_rating_helpfulness[node[0]].append(node[4])
    except KeyError:
        user_rating_helpfulness[node[0]] = [node[4]]

print("Writing node features", len(ratingstruct))

with open("rating.csv", "w+", newline='') as node_file:
    writer = csv.writer(node_file, delimiter=",")
    writer.writerow(["node", "column_1", "column_2"])

    for user_id in user_rating.keys():

        feature_vector = []

        rating_counts = Counter(user_rating[user_id])
        helpfulness_counts = Counter(user_rating_helpfulness[user_id])

        # 5 values for rating
        for i in range(1, 6):
            feature_vector.append(rating_counts[i] / len(user_rating[user_id]))

        # 5 values for rating
        for j in range(1, 6):
            feature_vector.append(helpfulness_counts[j] / len(user_rating_helpfulness[user_id]))

        writer.writerow([user_id] + feature_vector)
