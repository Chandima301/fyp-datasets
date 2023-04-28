import csv
import orjson
import gc
from sys import argv


def selected_paper_fos():
    count = 0
    author_affiliations = dict()
    with open("../../datasets/dblp_v14.txt", "r") as dblp_file:
        print("File opened")
        for line in dblp_file:
          #  print(line)
            paper_dict = orjson.loads(line[:-2])
            try:
                authors = paper_dict["authors"]
            except KeyError:
                # author key missing in data
                continue

            for f in authors:
                author_id, author_name, author_affiliation = f.values()
                try:
                    author_affiliations[author_affiliation] += 1
                except KeyError:
                    author_affiliations[author_affiliation] = 1

            if count % 100000 == 0:
                # print(len(filtered_items), len(items))
                gc.collect()

                print(count)
            count += 1

    print("Writing author affiliations")
    with open(f"author_affiliations.txt", "w+", newline='') as author_affiliations_file:
        writer = csv.writer(author_affiliations_file, delimiter=" ")
        for key, value in author_affiliations.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    selected_paper_fos()