import scipy.io as sio
import csv

print("Reading trust relations....")
mat_contents = sio.loadmat("epinion_trust_with_timestamp.mat")
print("Structure of trust relations")
print(mat_contents.keys())
print("")
print("Trust relations content")
truststruct = mat_contents['trust']
print(truststruct)

print("Writing edgelist", len(truststruct))
with open("epinion_trust_with_timestamp.txt", "w+", newline='') as edge_file:
    writer = csv.writer(edge_file, delimiter=" ")
    for edge in truststruct:
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

print("Writing node features", len(ratingstruct))
with open("rating_with_timestamp.txt", "w+", newline='') as node_file:
    writer = csv.writer(node_file, delimiter=" ")
    for node in ratingstruct:
        writer.writerow(node)